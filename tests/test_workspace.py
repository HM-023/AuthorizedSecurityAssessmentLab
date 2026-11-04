import tempfile
import unittest
from webapp.app import Workspace,redact,make_report,validate
BASE={'title':'Unsafe output','asset':'DEMO','severity':'high','status':'open','description':'Untrusted text rendered as markup','remediation':'Encode output by context'}
class FindingTests(unittest.TestCase):
    def test_resolution_requires_retest_and_preserves_identity(self):
        f=validate(BASE)
        with self.assertRaises(ValueError):validate({**BASE,'status':'resolved'},f)
        updated=validate({**BASE,'status':'resolved','retest_note':'Encoded markup displayed as plain text'},f)
        self.assertEqual(updated['id'],f['id']);self.assertEqual(updated['created'],f['created'])
    def test_redaction_of_identifiers_and_credentials(self):
        s=redact('a@example.com 203.0.113.8 password=abc Bearer secret-token ghp_example123')
        for item in ['a@example.com','203.0.113.8','abc','secret-token','ghp_example123']:self.assertNotIn(item,s)
    def test_report_html_escapes_and_redacts_user_content(self):
        f=validate({**BASE,'title':'<script>alert(1)</script>','evidence':'a@example.com token=secret'})
        r=make_report([f]);self.assertNotIn('<script>',r['html']);self.assertIn('&lt;script&gt;',r['html'])
        self.assertNotIn('a@example.com',r['markdown']);self.assertNotIn('token=secret',r['markdown'])
    def test_invalid_severity_is_rejected(self):
        with self.assertRaises(ValueError):validate({**BASE,'severity':'catastrophic'})
    def test_update_and_export_persist_without_duplicates(self):
        with tempfile.TemporaryDirectory() as d:
            w=Workspace(d);f=w.action({'action':'save','finding':BASE});f['status']='in_progress'
            w.action({'action':'save','finding':f})
            other=Workspace(d);self.assertEqual(len(other.state()['findings']),1)
            self.assertEqual(other.state()['findings'][0]['status'],'in_progress')
            self.assertEqual(other.action({'action':'export'})['count'],1)
