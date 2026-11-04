"""Local finding lifecycle and redacted Markdown/HTML report generation."""
import html
import re
import uuid
from webapp.runtime import Store, now, text, serve
SEVERITIES=['critical','high','medium','low','informational']
STATUSES=['open','in_progress','resolved','accepted']

def redact(value):
    value=re.sub(r'(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b','[EMAIL REDACTED]',str(value))
    value=re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b','[IP REDACTED]',value)
    value=re.sub(r'(?im)\b(?:bearer\s+)[A-Za-z0-9._~+/=-]+','Bearer [TOKEN REDACTED]',value)
    value=re.sub(r'(?im)\b(password|secret|api[_-]?key|token)\s*[:=]\s*[^\s,;]+',r'\1=[REDACTED]',value)
    value=re.sub(r'\bgh[pousr]_[A-Za-z0-9_]+\b','[TOKEN REDACTED]',value)
    return value

def validate(item,existing=None):
    if not isinstance(item,dict):raise ValueError('Expected an object')
    severity=item.get('severity','medium');status=item.get('status','open')
    if severity not in SEVERITIES:raise ValueError('Unknown severity')
    if status not in STATUSES:raise ValueError('Unknown finding status')
    fields={k:text(item.get(k),label,limit) for k,label,limit in [
      ('title','Title',160),('asset','Asset alias',100),('description','Description',6000),('remediation','Remediation',6000)]}
    for k in ['evidence','retest_note']:
        v=item.get(k,'')
        if not isinstance(v,str) or len(v)>6000:raise ValueError(f'{k} must be at most 6000 characters')
        fields[k]=v.strip()
    if status=='resolved' and not fields['retest_note']:raise ValueError('A retest note is required before resolving a finding')
    return {**fields,'id':existing['id'] if existing else str(uuid.uuid4()),'created':existing['created'] if existing else now(),
      'updated':now(),'severity':severity,'status':status,'severity_basis':'Manually assigned; not a calculated CVSS score'}

def make_report(findings,project='Authorized Lab Assessment',do_redact=True):
    title=text(project,'Report title',160)
    clean=redact if do_redact else str
    lines=[f'# {clean(title)}','','Local methodology workspace export. Manually assigned severity; no automated scanning or CVSS calculation.','',
      f'Generated: {now()}','',f'Findings: {len(findings)}','',
      'Redaction uses patterns and cannot guarantee anonymization. Review every export before sharing.','']
    for f in sorted(findings,key=lambda f:(SEVERITIES.index(f['severity']),f['title'])):
        lines.extend([f'## {clean(f["title"])}','',f'- ID: {f["id"]}',f'- Asset: {clean(f["asset"])}',f'- Severity: {f["severity"]}',f'- Status: {f["status"]}',''])
        for key,label in [('description','Observation'),('evidence','Evidence'),('remediation','Remediation'),('retest_note','Retest')]:
            lines.extend([f'### {label}','',clean(f.get(key,'')) or 'Not recorded.',''])
    markdown='\n'.join(lines)
    # HTML text is escaped before insertion; no user content is treated as markup.
    page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+'</title><style>body{font:15px system-ui;max-width:900px;margin:50px auto;padding:0 25px;line-height:1.7;color:#142033}pre{white-space:pre-wrap;overflow-wrap:anywhere}h1{font-size:32px}</style><body><h1>'+html.escape(clean(title))+'</h1><pre>'+html.escape(markdown)+'</pre></body></html>'
    return {'markdown':markdown,'html':page,'redacted':do_redact,'count':len(findings)}

class Workspace:
    def __init__(self,directory):self.store=Store(directory)
    def state(self):return {'kind':'assessment','title':'Assessment Workspace','subtitle':'Track findings from observation to retest, then export a clear, reviewable report.','category':'DEFENSIVE SECURITY','findings':self.store.all('finding'),'severities':SEVERITIES,'statuses':STATUSES}
    def action(self,body):
        action=body.get('action')
        if action=='save':
            item=body.get('finding',{});old=self.store.get('finding',item['id']) if item.get('id') else None
            return self.store.save('finding',validate(item,old))
        if action=='delete':self.store.delete('finding',body.get('id'));return {'ok':True}
        if action=='export':return make_report(self.store.all('finding'),body.get('title','Authorized Lab Assessment'),True)
        if action=='demo':
            if self.store.all('finding'):raise ValueError('Demo can only be added to an empty workspace')
            return self.store.save('finding',validate({'title':'Illustrative input handling review','asset':'LOCAL-DEMO-APP','severity':'medium','status':'open',
             'description':'Fictional example: a query-building pattern requires defensive review. No live target has been tested.',
             'remediation':'Use parameterized database access and verify input is treated as data.','evidence':'Illustrative record only; no test evidence attached.'}))
        raise ValueError('Unknown action')

if __name__=='__main__':serve(Workspace,8104)
