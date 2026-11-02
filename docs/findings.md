# Training-lab finding categories

The following categories were discussed/demonstrated in historical training-lab materials. They are not validated findings against a live target and have **no assigned CVSS scores** here.

| Category | What to inspect in the lab | Recommended fix | Retest |
|---|---|---|---|
| SQL injection | Database query built from untrusted web input | Parameterized queries, least-privilege database accounts, strict input handling | Verify data is treated as data rather than executable SQL |
| Cross-site scripting | User-controlled text interpreted as script in HTML context | Context-aware output encoding, template auto-escaping, CSP as defense in depth | Confirm unsafe markup is not executed in the browser |
| Missing security headers | Incomplete browser security policy | Configure relevant CSP, HSTS (HTTPS deployments), MIME sniffing protection and framing policy | Inspect actual response headers |
| Unnecessary network exposure | Services visible on interfaces where not required | Remove or bind services, network segmentation, host firewall controls | Confirm only intended endpoints are reachable |

**Evidence status:** source materials omitted for privacy, consent and safety review. These descriptions are a technical summary, not new test results.
