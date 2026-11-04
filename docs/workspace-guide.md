# Authorized Security Assessment Lab: workspace guide

## Start and stop

Use `python -m webapp.app` from the repository root and open the printed loopback address. Python 3.11 or later is the supported baseline. Use the virtual environment activation command for your operating system. The default port is 8104; `--port` changes it. `Ctrl+C` shuts down the server.

## Main workflow

1. Create a finding with an asset alias, observation, manually assigned severity and remediation. Evidence is optional; use minimal fictional or authorized text.
2. Update its lifecycle state. The available states are open, in progress, resolved and accepted. A resolved finding must include a retest note. The app enforces the presence of the note; it cannot establish whether a real retest occurred.
3. Export a report from **Reports & exports**. The current register is sorted by severity. Markdown and standalone HTML downloads contain no active user HTML; the HTML report escapes user content.
4. Export patterns redact email addresses, IPv4 addresses, bearer tokens, common key/value secret formats and GitHub-style token strings. This does not cover all sensitive data: IPv6, names, unusual credentials and contextual identifiers can remain. Review the export manually before sharing it.
5. Local records retain the entered text until edited or removed; export redaction does not redact the database. SQLite is not encrypted by this app. Keep the data directory under your operating system's normal protection.
6. Finding edits replace the current record. This is not an immutable finding-version history or a certified assessment system. The application performs no target scanning.

## Local data and backups

Records live in `data/workspace.sqlite3` by default. ML model artifacts additionally live in `data/models/`. These paths are excluded from git. The file formats contain local workspace information and are not encrypted by the application. Stop the server before copying the entire data directory for a simple backup, then use `--data-dir` to reopen that copy. Deleting the data directory while the server is stopped resets the workspace. Exported files are saved wherever the browser downloads them; this app does not automatically publish them.

## Local browser boundary

Use the exact printed localhost/127.0.0.1 URL and reload after restarting the server. A new random session token is issued each time. There is no remote bind option. Host checks resist DNS rebinding, and API requests require the page's token. This is a browser-request boundary, not account authentication and not a defense against other software already running as the same operating-system user.

## Browser verification

GitHub Actions runs the end-to-end journey in `tests/browser.cjs` using pinned Playwright 1.56.1. It exercises real forms and local API actions, checks browser errors and mobile viewport fit, reloads persisted state and captures desktop/mobile PNGs. Screenshots use only synthetic or fictional inputs.
