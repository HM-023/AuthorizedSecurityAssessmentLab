# Authorized lab scope and methodology

## Rules of engagement

- Test only local virtual machines or intentionally vulnerable training applications under the operator's control.
- Define target IPs and accounts in a private authorization document; do not include live targets or tokens in a public repository.
- Stop if the test environment unexpectedly bridges to production networks.
- Preserve relevant timestamps, tool versions and non-sensitive redacted evidence privately.
- Do not retain private data that was exposed during tests; record the minimum needed for remediation.

## Assessment phases

1. **Asset discovery:** inventory lab systems and identify intended software.
2. **Configuration assessment:** review exposed services, authentication and headers.
3. **Controlled verification:** validate suspected issues manually and minimally on the authorized lab target.
4. **Risk evaluation:** describe preconditions, impact, exploitability and defensive boundaries.
5. **Reporting:** give reproducible *defensive* evidence and mitigation advice without secrets.
6. **Retesting:** record whether the application behavior changes after a fix.

Original reports sometimes referenced public services; those portions are intentionally excluded from this publication. Historic observations are not evidence of present-day vulnerabilities in any third-party system.
