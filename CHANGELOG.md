# Changelog

## 1.0.0 — Local workspace release (2026-11-04)

- Finding register: Create and edit observations, asset aliases, severity, evidence and remediation.
- Lifecycle tracking: Move findings through open, in progress, resolved or accepted states.
- Retest gate: Require a retest note before a finding can be marked resolved.
- Report generation: Export a severity-ordered Markdown report and escaped standalone HTML.
- Pattern redaction: Mask email, IPv4 and common credential patterns in exports.
- Local persistence: Keep the current finding register in SQLite and use fictional demo data only on request.
- Added a responsive local dashboard, request-boundary validation, ignored local state, regression tests and browser workflow verification.
- Preserved the prior case-study material and its contribution/reuse limitations.

Remaining scope: This app organizes assessment records; it does not scan or test targets. Severity is manually assigned, not a calculated CVSS score. Redaction is pattern-based and incomplete, so every report needs review before sharing.
