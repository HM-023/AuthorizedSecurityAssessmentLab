# Defender retest checklist

- [ ] Software versions and application endpoints are documented privately.
- [ ] Database access uses parameterized queries and low-privilege roles.
- [ ] Untrusted content is encoded for the specific output context.
- [ ] Browser policies match the deployment's real needs and have been tested for regressions.
- [ ] Unnecessary ports and services have been removed or tightly scoped.
- [ ] Test accounts, lab credentials, database snapshots and session tokens have been reset/removed.
- [ ] All evidence has been minimized and checked for personal/sensitive content before sharing.
- [ ] Every finding records a retest status rather than assuming remediation worked.
