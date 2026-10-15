# GEASS prototype — spec

Labels: ready-for-agent
Status: ready-for-agent
Tracker: local markdown (`.scratch/geass/`)

Source of truth for the product: `geass_prd_master_implementation_plan.md`, treated as a **draft to triage**. Chartering research has shown it stale in four load-bearing places; where this spec and the PRD disagree, this spec wins.

## Problem Statement

Indonesian public procurement publishes a great deal and explains very little. **SIRUP** exposes every planned package — `id_rup`, `nama_paket`, `satker`, `total_pagu`, `uraian_pekerjaan`, `volume_pekerjaan` — and **LPSE/SPSE** exposes what happened to those packages afterwards. Both are nominally open. Neither is *readable*.

So the finding a citizen, journalist or auditor actually wants is buried under work that no individual can do by hand:

- **The wrapper title hides the purchase.** `nama_paket` reads *"Belanja Alat/Bahan untuk Kegiatan Kantor Lainnya"*; only `uraian_pekerjaan` reveals karangan bunga or dekorasi resepsi. You have to open packages one at a time to see this, and there are hundreds of thousands of them.
- **Nothing is priced against a statute.** Regional **SSH/SBU** caps exist as PDFs on **JDIH** portals. Comparing a package's implied unit price to its statutory ceiling is a manual, per-package, per-region research task that currently takes an afternoon for one row.
- **Execution-stage behaviour is invisible in aggregate.** Who bid, who was disqualified, and why, and who won at what share of **HPS** — these are public tabular records, but they exist per tender on one of hundreds of regional portal hosts, and nobody joins them across an agency.
- **Planning and execution are never read together.** A curious planning package and the tender that executed it sit in two systems with no obvious bridge, so "this budget became that contract" is a claim people assert rather than demonstrate.
- **The output of a finding is a request, and that paperwork is the friction.** Converting a suspicion into a legally-formed **PPID** information request under UU No. 14/2008, or into an **APIP/BPK** risk brief, is skilled clerical work that stalls most leads before anyone acts on them.

The affected people are specific: **investigative journalists and civic watchdogs** who need a defensible lead rather than a spreadsheet; **regional inspectors (APIP) and BPK auditors** who must prioritise before an annual evaluation; and **ordinary citizens**, who currently have no way to see how local tax money was spent in a form they can understand.

The second problem is the build's own. The team is entering the Google Cloud AI Builder Cup 2026, has roughly three working days, and is judged on four weighted criteria: **Technical Merit & Gen AI Implementation (40%)**, Problem Alignment & Impact (25%), Innovation & Creativity (25%), and UX & Solution Design (10%). The PRD proposes seven expensive things and a four-day plan that no longer exists. The prototype has to be built **and** deployable, because a submission missing any one of its artifacts is forfeit.

## Solution

A single deployed surveillance service, **GEASS** — Government Expenditure Anomaly & Syndicate Surveillance — that turns public Indonesian procurement data into **checkable risk signals and one-tap information requests**. It never states that a named party did anything wrong.

One Cloud Run service serves both the JSON API and a dark-mode, high-density frontend:

- **The Absurdity & Markup Radar** — a filterable table of SIRUP packages, each carrying an AI classification from a fixed five-class taxonomy, the implied unit price in **IDR**, the statutory **SSH** cap it was compared against, and the delta between them. Vague wrapper naming is shown *next to* the true underlying item so concealment is visible in one line.
- **The forensic drawer** — opened from a row. It contains the price forensics (implied unit price vs SSH cap vs residual benchmark, in IDR), the prosecutor-versus-defense reasoning, the **LPSE** execution view for the linked tender, and the syndicate graph for that tender's participants.
- **One-tap action** — generate a draft **Surat Permohonan Informasi Publik (PPID)** or an **APIP/BPK** risk brief as a dossier. These ask for documents. They do not allege.
- **A security beat that is real, not staged** — **Model Armor** guards ingestion, so an injection hidden inside `spesifikasi_pekerjaan` or an uploaded KAK is intercepted before it reaches the model. A toggle makes the guard demonstrable on stage.
- **A telemetry panel** — Cloud Trace spans for the run, visible in the product rather than only in the console.

Every claim the product surfaces carries **provenance**: which stage produced it, from which source, and whether the number was computed by deterministic SQL or asserted by a model. The neuro-symbolic boundary is enforced structurally — **the model never produces a number that appears in the UI.**

## User Stories

### Retrieval and ingestion

1. As an investigative journalist, I want SIRUP packages for a chosen region and budget year retrieved from the live source, so that my leads reflect current data rather than a stale snapshot.
2. As an investigative journalist, I want `uraian_pekerjaan`, `spesifikasi_pekerjaan` and `volume_pekerjaan` extracted for each package, so that the real object of expenditure is visible instead of only the administrative wrapper title.
3. As a build agent, I want to crawl at a polite, fixed request rate with a bounded per-package detail budget, so that the source stays available and the run still finishes inside the window.
4. As a build agent, I want throughput and field-completeness reported after the first two working hours, so that the abundance fallback trigger can be evaluated against a number instead of a feeling.
5. As an investigative journalist, I want volume seeded in bulk from LKPP's open XLSX exports alongside a targeted detail crawl, so that breadth does not cost one request per package.
6. As an investigative journalist, I want LPSE tender records — announcement, participants, evaluations, winner and schedule — retrieved for a set of tenders, so that execution-stage behaviour is available, not just planning.
7. As a build agent, I want institution names resolved to LPSE host slugs and a nationwide host available, so that retrieval works across separately operated regional portals.
8. As a build agent, I want retrieval to run through a maintained library rather than a bespoke scraper, so that field coverage and rate limiting are someone else's tested problem.
9. As an auditor, I want current-year regional SSH retrieved as structured `harga_satuan_maksimum` rows, so that price grounding rests on a real statute for the demo region.
10. As an auditor, I want to know which SSH document grounds a given package, so that a benchmark is traceable to its regulation rather than to vibes.
11. As an auditor, I want a package to record that no SSH cap was found when none exists, so that a missing benchmark is visible rather than silently treated as normal.
12. As an investigative journalist, I want ingestion to refuse and report a non-200 or malformed source response rather than writing an empty record, so that the dataset never quietly degrades.

### Classification and normalisation

13. As an investigative journalist, I want a vague `nama_paket` shown beside the normalised underlying item, so that concealment by naming is legible in a single line.
14. As an investigative journalist, I want each package classified as `ABSURD`, `INDICATED MARKUP`, `SPECIFICATION LOCK`, `SPLIT PACKAGE` or `NORMAL`, so that triage does not require reading raw fields.
15. As an investigative journalist, I want the classification to come with reasoning in Indonesian, so that a lead is intelligible to the audience it is for.
16. As an auditor, I want the agency's `satker` and administrative tier shown next to the classification, so that a mandate mismatch is judged in context rather than in the abstract.
17. As an auditor, I want `Pecah Paket` detected from near-identical packages sitting just below the direct-appointment threshold, so that threshold-avoidance is a signal rather than a suspicion.
18. As an investigative journalist, I want specification-lock detected from brand-pointing or restrictive specification text, so that tailored requirements are flagged before tender.
19. As a build agent, I want classification outputs validated against a schema, so that a malformed model response becomes a recorded failure rather than a corrupt row.
20. As a build agent, I want the model to receive only the fields it needs, so that irrelevant text cannot steer a classification.

### Price grounding

21. As an investigative journalist, I want the **implied unit price** computed from `total_pagu` and the parsed numeric volume, so that disproportion is a number in IDR rather than an adjective.
22. As an investigative journalist, I want the implied unit price compared against the statutory SSH cap with the delta shown in IDR, so that a markup claim is directly checkable.
23. As an investigative journalist, I want to see the exact regulation that supplied a benchmark price, so that I can cite it.
24. As an auditor, I want unparseable or absurd volumes (e.g. `"1 Paket"` with no itemisation) recorded as ungrounded rather than silently coerced into a quantity, so that a computed delta is never built on a guessed denominator.
25. As an auditor, I want every IDR figure in the UI to originate from deterministic computation, so that AI-derived arithmetic can never be mistaken for evidence.
26. As an auditor, I want the residual retail comparison shown only where an SSH cap is genuinely absent, so that a market benchmark does not crowd out the statutory one.

### Execution forensics and the syndicate graph

27. As an investigative journalist, I want a flagged package tied to its downstream tender where a real join exists, so that the planning-to-execution claim is demonstrated rather than asserted.
28. As an investigative journalist, I want the product to say plainly when no join exists and present the two sides side by side instead, so that the demo never overclaims lifecycle tracking.
29. As an investigative journalist, I want participants, evaluation outcomes, disqualification reasons and winner surfaced per tender, so that the public record of what happened is readable in one view.
30. As an investigative journalist, I want a **high-bid winner** signal where cheaper bidders were disqualified, so that the most legible execution anomaly is visible without manual comparison.
31. As an investigative journalist, I want a **cover-bidding** signal where the same set of vendors repeatedly appears together, so that a pattern across tenders is surfaced rather than one tender in isolation.
32. As an investigative journalist, I want vendor identity clustered across masked NPWP prefixes and normalised name variants, so that the same company under two names is one node.
33. As an investigative journalist, I want candidate shared-address clusters surfaced for manual review, so that address overlap is presented as something to check rather than as proof of collusion.
34. As an investigative journalist, I want the syndicate graph rendered for one tender, so that relationships between satker, package, winner, disqualified bidders and shared identifiers are seen at once.
35. As a competition judge, I want the graph to load quickly and read clearly at video resolution, so that the most differentiating idea in the demo is actually visible.

### Adversarial verification and security

36. As an auditor, I want every accusatory-shaped badge to first survive a prosecutor-versus-defense review, so that a defensible exception can remove a finding before I ever see it.
37. As a build agent, I want the adversarial loop to have a hard stop condition on turns and tokens, so that it cannot consume the run's budget.
38. As an auditor, I want the defense's rebuttal retained as evidence alongside the finding, so that a surviving signal arrives with its counter-argument attached.
39. As a security-minded judge, I want Model Armor to inspect the incoming `spesifikasi_pekerjaan` and any uploaded document, so that a hidden instruction cannot force a package to be classified `NORMAL`.
40. As a security-minded judge, I want the guard demonstrable on demand with a poisoned specimen, so that the control is verifiable rather than described.
41. As an auditor, I want a blocked input recorded with what was intercepted, so that the defence is auditable rather than invisible.

### Dossier and civic action

42. As an investigative journalist, I want a one-tap draft **PPID** information request for a flagged `id_rup`, so that the step that normally stalls a lead takes seconds.
43. As an auditor, I want a one-tap **APIP/BPK** risk brief covering the package, its markup delta in IDR and any vendor-graph anomalies, so that a finding arrives in a form I can forward.
44. As an auditor, I want every generated document to be phrased as a **request for information** and never as an allegation of wrongdoing, so that using it does not expose me.
45. As an auditor, I want the dossier to state the provenance of each claim it contains, so that a recipient can check it.

### Governance, interface and operations

46. As an ordinary citizen, I want a zero-login dark dashboard I can open and understand, so that I can see how local tax money was spent without a procurement background.
47. As an ordinary citizen, I want filters by region, agency type and anomaly class, so that I can narrow to my own area.
48. As a competition judge, I want to see that a substantial volume of real records sits behind the table, so that the problem's scale is credible.
49. As a competition judge, I want to see live cloud execution traces inside the product, so that Google Cloud usage is self-evident rather than asserted.
50. As a build agent, I want an explicit and labelled inventory of anything stubbed for the demo, so that no stub is accidentally presented as a working system.
51. As a build agent, I want retrieval, inference and storage to share one deployable artifact, so that a three-day build has one deployment surface instead of three.
52. As a build agent, I want the whole pipeline runnable against recorded payloads with no network access, so that I get deterministic runs and a test suite that costs nothing.
53. As a build agent, I want a hard cap on model calls per run and a deterministic pre-filter before inference, so that the build cannot exhaust its cloud credit before the demo is recorded.
54. As a build agent, I want the deployed service reachable from outside the builder's network without authentication, so that a judge can open it on the day.
55. As a build agent, I want the service to degrade visibly rather than fail silently when a data source is unreachable at judging time, so that a demo survives a dead upstream.

## Implementation Decisions

### Scope: all four modules appear, each scoped down

The PRD's four modules all ship, deliberately narrower:

- **Module 1 (Radar)** keeps the full five-class taxonomy and all three detection capabilities. Grounding is against real **SSH** statute for one region rather than national coverage.
- **Module 2 (Syndicate graph)** ships against a **small, hand-verified set of real tenders**, not national breadth. The graph is a **rendered node-link view**, not a force-directed interactive canvas. Interactivity is explicitly traded away.
- **Module 3 (Adversarial + Model Armor)** keeps both halves. Model Armor is a **real pre-ingestion guard** with a demonstrable toggle, not a simulation.
- **Module 4 (Dossier)** ships the PPID request and the risk brief as generated artifacts.

No 5,000-row live crawl is a goal in itself. Breadth is a means to credibility, not a deliverable.

### Region and demo scope

**Kab. Sukoharjo, Jawa Tengah** is the grounding region, because current-year statutory SSH exists for it by name (Perbup Sukoharjo No. 2/2026, SSH TA 2026) and it is the region the PRD's anchor cases sit in. Provincial (Jawa Tengah) documents are the fallback tier. National aggregators are used for *discovery* of documents, not for coverage claims.

The single anchor case is **not** fixed here; it is whatever *Verify the PRD's anchor anomalies* proves exists, and it must have a real downstream LPSE tender if a lifecycle claim is to appear on screen.

### Data retrieval route

- **SIRUP**: live HTML crawl of `sirup.inaproc.id`, accepting one request per package for the detail fields. The sanctioned INAPROC API is access-gated and is treated as a hedge, never as the plan. LKPP's open XLSX exports seed volume cheaply. The settled **fallback trigger** applies: if within the first two working hours the detail route cannot deliver roughly 200 packages with `uraian_pekerjaan` populated, breadth-first crawling is abandoned for a real slice plus curated anchors.
- **LPSE/SPSE**: retrieved through **PyProc**, which is pinned to an exact version and treated as replaceable behind a thin internal wrapper. Its MCP server is used as a real MCP surface, not as decoration.
- **JDIH**: SSH documents discovered via provincial subject indexes and the national BPK aggregator, then extracted to structured rows. Whether the PDFs carry a text layer is verified against one real file *before* any grounding claim is scripted; a scan-only document forces a pre-extracted table instead of a RAG datastore.
- Rate limits are respected by default (≈1 request/second) and the crawler identifies itself. Bulk scraping of government portals is defensible only if it is polite.

### Storage and the neuro-symbolic boundary

**BigQuery is the store of record**, for the seeded demo dataset and for graph traversal (BigQuery Graph is GA). This closes the map's *"where data lives"* fog: there is no local store with BigQuery bolted on.

Tables mirror the domain field names: SIRUP packages, LPSE tenders, LPSE participants, SSH price caps, and a classifications/signals table. Money is stored and serialised as **integer IDR NUMERIC — never floating point**, because the entire evidentiary claim is that currency arithmetic is exact and deterministic.

The boundary is a contract, not a convention:

> **Gemini extracts and classifies. SQL and Python compute.**
>
> Every figure rendered in IDR is produced by deterministic code from stored values. No number shown to a user is ever taken from model output.

Model output is limited to: a normalised item, a quantity candidate, a unit candidate, a taxonomy label from a closed enum, and free-text reasoning. Every one of those is schema-validated on arrival, and a validation failure is recorded as a failure rather than coerced.

### The API is the seam

The service's HTTP JSON surface is the sole integration boundary, and the spec fixes its resource shape:

- a package listing with filters (region, agency type, anomaly class) and paging;
- a package detail returning the classification, provenance, price forensics and the linkage state to any downstream tender;
- a tender execution view returning participants, evaluations, disqualification reasons, winner and bid-to-HPS ratios;
- a graph resource for one tender;
- a dossier generation action returning the rendered document;
- an ingestion trigger that accepts a **fixture mode**, so a run against recorded payloads requires no network;
- a run/trace resource exposing the spans the telemetry panel renders;
- a health/readiness resource that reports per-source reachability.

Serialisation follows the domain's own `snake_case` field names (`id_rup`, `total_pagu`, `nama_pemenang`). Every analytic payload carries a **provenance envelope**: producing stage, source identifier, retrieval timestamp, and a flag distinguishing computed from model-asserted.

### Integrity controls (binding on everything that publishes)

The line drawn by *Integrity and defamation stance* governs, and until that ticket resolves the following safe defaults are binding rather than optional:

- Nothing the system generates asserts wrongdoing. The PPID artifact is a **request for information** under UU No. 14/2008; the risk brief reports deltas and patterns.
- A unit price above SSH is presented as a **delta from a statutory benchmark**, never as intent. Procurement error is a live explanation and the language must leave room for it.
- A single build flag switches vendor and agency names to anonymised identifiers, so if the stance demands it, the public surface can be anonymised without a rewrite.
- Address overlap and NPWP-prefix clustering are surfaced as **clusters to review**, never as findings of collusion.
- Anything a human must approve before publication is visible in the product; if nothing requires approval, the product does not claim human-in-the-loop governance.

### Model and agent topology

The PRD's five-agent ADK diagram is **not** inherited as-is. Judges read the repository, so the topology has to be defensible as architecture rather than flattering as a diagram. The count and the split are settled by *Architecture lock* before the agent layer is built; this spec fixes only the constraints that ticket must satisfy:

- stages are named, typed and separately traceable, each with a declared input and output schema;
- ADK is the orchestration layer and the service deploys to Cloud Run;
- the adversarial prosecutor/defense loop is bounded by an explicit turn and token stop condition;
- no stage may emit unvalidated free text into a user-visible surface;
- the model/SQL boundary is enforced as described above, and a technical judge probing it finds it structural.

### Budget and cost control

The entire cloud budget is **$300 over 90 days**. Therefore:

- a deterministic pre-filter narrows the corpus to candidate anomalies before any model call;
- a hard cap on model calls per run fails the run loudly rather than spending past a threshold;
- the full-corpus classification pass is a bounded, counted operation, not an ambient one;
- model tiering is explicit — the cheap model for extraction and normalisation, the stronger model only where classification genuinely needs it.

### Deployment

One Cloud Run service serves the JSON API, the frontend, and the trace panel. The UI is server-rendered with a small amount of client-side JavaScript for the drawer and the graph — no second deployable, no second CI surface, no second contract. The deployed URL is the judged surface, must be reachable without authentication, and must report per-source health so that a dead upstream degrades visibly rather than returning an empty table.

## Testing Decisions

**The seam, and why there is only one.** The system is cut open at exactly one place: **the service's HTTP JSON API**. Everything above ingestion — classification, grounding, the graph, the dossier, the security gate — is asserted by driving the running service. The frontend is driven through that *same* seam with a browser, not through a stubbed second API; a separate UI contract is the thing that makes demo interfaces rot fastest, and it is not worth a second contract in three days.

Crawler field-extraction is the deliberate exception and is **not** given an injectable port. Parsers that turn a raw payload into a typed record are tested directly as pure functions against recorded fixtures, using the same fixture mode the ingest endpoint accepts. The accepted cost of this decision: scraper breakage surfaces at the API level plus the parser tests, rather than at a dedicated source boundary.

**What makes a good test here.**

- Tests assert **external behaviour**: HTTP status, resource shape, field values, enum membership. Never internal function calls, never prompt text.
- Tests never assert on a model's prose. They assert on structure — that a label is one of the five, that reasoning is non-empty, that a validation failure was recorded — and on numbers, which are only ever deterministic.
- Tests never hit the network. Fixtures are recorded once from live sources, trimmed to small specimens, and committed. Live tests, if any, are marked and excluded from the default run.
- Tests assert the **provenance envelope** is present and self-consistent, because provenance is the feature that keeps the integrity claims true.
- Tests assert the **neuro-symbolic boundary** directly: a stubbed model that returns a numeric-looking claim must not change any IDR figure the API reports.
- Tests assert **integrity defaults** hold: no generated dossier contains an assertion of wrongdoing, and with the anonymisation flag set no real vendor or agency name appears in a response.
- A test that a source is unreachable and the service reports degraded health rather than serving an empty success.

**Modules tested.** The service end to end through its HTTP surface (listing with filters, detail, tender execution, graph, dossier, ingest in fixture mode, trace, health). The crawler and SSH parsers as pure functions. The frontend flows the demo depends on: filtering the radar, opening a drawer, reading price forensics, triggering the Model Armor block, and generating a dossier.

**Prior art.** None — this is greenfield, with no existing test suite and no ADRs to respect. This spec establishes the convention: a Python test suite for the service and the parsers, and a small browser-driven suite for the demo-critical flows, both runnable offline by default.

## Out of Scope

Consciously excluded, and not to be quietly reintroduced:

- **The AHU corporate enrichment dropzone** — director, commissioner and notary extraction from uploaded deeds. Needs documents only auditors and journalists hold.
- **Year-over-year budget inflation tracking** across `tahun_anggaran`.
- **National-scale coverage.** "Three million rows a year" is the problem statement, not the build target.
- **An interactive force-directed canvas graph.** The graph is rendered; it is not a physics playground.
- **Post-competition productisation** — no hardening, onboarding, user accounts or multi-tenancy.
- **Live retail price scraping** beyond what SSH grounding genuinely needs.
- **The retired `sirup.lkpp.go.id` domain and the PRD's "public JSON endpoints" premise** — superseded by the INAPROC migration and retained only as historical context.
- **The demo video, the deck, the public repository and the submission form.** Those are the wayfinder map's own tickets (*The three-minute demo narrative*, *Package and submit*), which own them; this spec stops at a deployed, working prototype.

## Further Notes

**This spec is published before *Architecture lock* resolves.** That ticket owns the agent topology, the adversarial loop's stop condition, the stub inventory, and the exact deployment split. Where it decides differently from the *Model and agent topology* section above, **it amends this spec** rather than duplicating it — the build should follow ticket 08 and this spec's constraints together, not one against the other. Ticket 08 is in turn blocked on *Provision the Google Cloud project*, which no agent can complete alone: there is no GCP project, no billing, and no `gcloud` on this machine today, so nothing deploys until a human opens that gate.

**Two open tickets can change what the demo claims, not just how it looks.** *Does id_rup join to kode_lelang?* decides whether lifecycle tracking is a demonstrated join or an honest side-by-side. *Verify the PRD's anchor anomalies* decides whether any of the PRD's named cases survive — none could be confirmed, and a hero case a judge can look up and find wrong is worse than no hero case. Both are cheaper to resolve now than to discover at video-recording time.

**Facts dated 15 Oct 2026, re-check anything load-bearing.** The submission window and rubric were read from primary sources and can move. The Google product names have already drifted away from the PRD's vocabulary — the deck and the video will name this stack, and stale product names read as a team that has not touched the platform. Exact Gemini model IDs must be pinned at build time.

**Two fidelity risks are unresolved and must not be papered over.** Whether the SSH PDFs carry a text layer, and whether `alasan_gugur` text is rich enough for a model to add anything over a keyword match. If disqualification text proves thin, high-bid-winner detection is a deterministic comparison and the spec should say so rather than dress it as analysis. Maps Places geocoding remains unpriced and unverified; address-overlap detection must degrade to fuzzy string matching if it is not affordable.

**One dependency carries maintenance risk.** LPSE retrieval rests on a third-party library rather than first-party access. Pin it, wrap it thin, and be ready to vendor it — a public repository will be judged on whether it still resolves in six months.

**Cheap hedge worth taking immediately.** The INAPROC Data Integrator access request costs a letter and unknown latency. It is off the critical path; the crawl proceeds regardless. Its own ticket owns it.
