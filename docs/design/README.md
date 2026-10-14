# GEASS UI draft — Evidence desk

Status: design proposal, 2026-10-14. Open [the interactive preview](preview.html) in a browser. It works from disk, has no dependencies or external requests, and contains synthetic data only. It does not create the React/Vite application, authenticate anyone, publish a finding, or execute analysis.

![Static radar concept, with synthetic records](radar-concept.png)

This is a static concept rendering rather than a browser screenshot. The HTML includes the case investigation and reviewer workspace as well as the radar.

## Direction

1. Help journalists and inspectors move from a procurement lead to inspectable evidence.
2. Tone: deliberate, factual, restrained. Indonesian product language.
3. Layout: horizontal workspace navigation, dense public radar, full-width investigation, private review desk.
4. Typography: system sans-serif for readable evidence; system monospace for identifiers, amounts and source locators. No font download.
5. Surfaces: ink navy canvas, slate panels, warm-white type, amber signals, mint verified observations. No glowing risk badges or decorative gradients.
6. Motion: short state changes only; honor reduced motion. No animated surveillance theater.
7. Signature: an **evidence rail** that follows each finding from planning capture to benchmark, execution coverage, and review. Gaps are visible beside the claim rather than buried in a disclaimer.

## Authority and scope

- [Demo specification](../../.scratch/geass-wayfinding/spec.md) governs behavior; [build plan](../geass-build-plan.md) governs sequence.
- [Focused demo](../adr/0001-focused-evidence-demo.md): no invented national counts, authentic case claims, or committed region.
- [One deployment](../adr/0002-google-cloud-single-deployment.md): later implementation is React/TypeScript/Vite with FastAPI on Cloud Run. This dependency-free HTML is a throwaway review artifact.
- [Human review](../adr/0003-review-before-publication.md): private drafts and public approved versions are distinct. Reviewer navigation here is a labeled role simulation, not authentication.
- [Bounded analysis](../adr/0004-bounded-resumable-analysis.md): public reading never triggers analysis; inspector reports simulated stages only.
- [Evidence abstention](../adr/0005-evidence-and-deterministic-signals.md): insufficient evidence and not assessed remain distinct from normal.
- [SQL graph and Markdown](../adr/0006-sql-graph-and-draft-dossiers.md): observed edges, accessible relation table, draft downloads; no ownership inference or PDF action.

## Screen and interaction inventory

| Screen | Hierarchy | Draft interactions |
| --- | --- | --- |
| Radar publik | Scope → approved record counts → labeled search/filters → table → pagination | Search/filter synthetic records; open a case; loading/empty/error state controls |
| Penelusuran kasus | Version/status → planning ceiling and coverage → evidence rail → benchmark/counterevidence → execution graph → draft action | Source locator dialog; accessible graph table; benchmark abstention; draft preview and Markdown sample download |
| Ruang reviewer | Role simulation → selected draft version → evidence/review readiness → decision reason → approve/reject actions | Simulate a local decision; approval requires a reason and complete reviewable evidence; reset demo |
| Inspector | Stage outcomes and integration boundary | Expand simulated pipeline; no Cloud Console links or private traces |

The public radar includes reviewed synthetic records with supported and insufficient-evidence states; it does not expose the private draft. Local reviewer actions deliberately do not mutate the public radar: the preview illustrates review feedback, not a publication backend. Real implementation binds approval to an exact version and invalidates public/download access on withdrawal.

## Design tokens

| Role | Value |
| --- | --- |
| Canvas / panel / raised surface | `#0c1420` / `#121e2d` / `#192838` |
| Primary / secondary text | `#edf2f7` / `#b2c0ce` |
| Quiet text / borders | `#93a7bc` / `#314358` |
| Amber lead / amber surface | `#f4c16b` / `#30291f` |
| Mint observation / mint surface | `#93d5bc` / `#19312d` |
| Error / focus | `#ffb5ac` / `#b6d7ff` |
| Spacing | 4, 8, 12, 16, 24, 32, 48 px |
| Type | 12 px locator, 14 px table/body support, 16 px body, 24 px section, 38 px page title |
| Radius | 4 px controls, 8 px panels; hierarchy comes from alignment and borders |
| Interaction | 44 px primary control targets; visible 2 px focus ring; 140 ms state transitions |

Numeric columns align right; identifiers and monetary values use tabular figures. Risk labels always include words. Approved status is separate from signal evidence status. Main body text is at least 14 px; mobile body text is 16 px. Primary controls remain usable on touch devices.

## Responsive and accessible behavior

- At desktop widths the radar keeps its tabular structure and the case uses a broad evidence column plus a narrow source/action rail.
- Below 900 px case and review columns stack; navigation and filter controls wrap. Below 640 px the radar becomes labeled cards rather than requiring horizontal table scrolling.
- Graph is an illustrative SVG, accompanied by an actual HTML relationship table. No information depends on graph position, hover, or color.
- Use a skip link, landmarks, native buttons/selects, visible labels, focus rings, `aria-current` navigation, live status announcements, and native dialogs with Escape support and restored focus.
- Loading, retry, empty search, insufficient evidence, unavailable graph, and review-conflict/quarantine messaging belong to implementation acceptance; the preview illustrates the first five and local review success/error states.
- Source dialogs contain fictional locators marked as samples. They are not fake links to real official documents. Default case data is invented and never reuses the PRD's unverified IDs/allegations.

## Review and later implementation

Validate hierarchy and wording here before visual details become production components. Later reuse tokens and information hierarchy in the agreed React/Vite stack; keep application authorization, version checks, screening enforcement and cloud integrations in their proper backend boundaries. This draft adds no services or dependencies.

No targeted external component inspiration was needed. Preview behavior and responsive checks are recorded in [validation](validation.md).
