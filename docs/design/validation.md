# Design draft validation

Draft baseline: 2026-10-14 (Asia/Jakarta). Validation completed during the October 14–15 session.

## Checked

- Static JavaScript syntax compilation with the existing bundled Node runtime.
- Assert-based fixture checks: six distinct synthetic public IDs, three supported signals, two insufficient-evidence cases, one limited normal case, positive integer sample amounts, and exclusion of the private reviewer draft from public radar fixtures.
- Static element identifiers, label associations and literal script element references.
- Offline preview: no external script/font/style requests, fetch calls or remote URLs.
- Text-token contrast against intended surfaces: each checked combination meets at least 4.5:1. This is a token check, not complete rendered accessibility certification.
- Reduced-motion rule, native dialog, labeled fields, graph text alternative, visible focus and narrow-screen card/stack rules reviewed in source.
- [Radar concept](radar-concept.png) visually inspected for legible hierarchy, synthetic-data disclosure and restrained color. It is an illustrative static rendering using the same fixtures, not a browser screenshot and not proof that HTML matches pixel-for-pixel.
- Documentation links and Git whitespace checked before commit.

Run the static self-check with `node docs/design/check-draft.cjs`. No package installation is required.

## Not verified

The browser tool rejected the local `file:` URL because its protocol policy permits only HTTP/HTTPS. No alternative browser surface, proxy or server was used to circumvent that rejection. Browser visual checks, responsive viewport rendering, keyboard/focus behavior, filter/navigation interactions and actual Markdown downloads are therefore unverified.

The design contains no real data, authentication, backend enforcement or cloud integration. Reviewer feedback is an in-memory simulation; changing roles is not an authorization boundary. These belong to implementation acceptance, not to this preview's validation claims.
