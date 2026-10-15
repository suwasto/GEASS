# Wayfinder map — GEASS: a judged AI Builder Cup 2026 entry by 18 Oct

Labels: wayfinder:map
Tracker: local markdown (`.scratch/geass/`)

## Destination

A submitted, judged Google Cloud AI Builder Cup 2026 entry by **18 Oct 2026**: GEASS deployed and publicly reachable on Cloud Run, a public GitHub repo, a deck, and a demo video under three minutes. All four, because submissions are graded on all four and a missing artifact forfeits the entry.

Execution is carried in this map. This effort overrides the usual "plan, don't do" posture: the tickets below end in a deployed, submitted prototype rather than a spec handed onward.

## Notes

**Domain.** GEASS — Government Expenditure Anomaly & Syndicate Surveillance. Indonesian public procurement. Two data planes: pre-tender planning on **SIRUP** and tender execution on **LPSE/SPSE**, plus statutory price caps published as **JDIH** Pergub/Perbup/Perwali SSH & SBU documents. The product source of truth is `geass_prd_master_implementation_plan.md` at the repo root, treated as a **draft to triage**, not a spec to honour. Chartering research has already shown it is stale in several places — see *Decisions so far* before trusting any detail in it.

**Skills every session should consult.** `grilling` + `domain-modeling` for anything in doubt; `research` for research tickets; `prototype` for prototype tickets.

**Standing decisions taken while charting (15 Oct).**
- The destination is a submitted entry, not a spec, so execution lives inside this map.
- **Scope: all four PRD modules appear in the demo, each scoped down.** No live crawl of 5,000 rows as a goal in itself. No force-directed canvas. The syndicate graph ships against a small, hand-verified tender set. Model Armor is a short security beat.
- **Data posture: live crawl, breadth-first.** Chartered research has since revised *how* that is achievable — see *SIRUP retrieval feasibility* — without overturning the goal.
- **Build split: the agent builds the prototype end to end.** The team owns review, the demo video, the deck, and the act of submitting.
- **Tracker: local markdown here.** The public GitHub repo is created only at submission time.
- **Start the INAPROC access request immediately**, in parallel with everything else. It is a cheap hedge on a process whose latency is unknown, and it is off the critical path.

**Risks carried explicitly, not buried.**
- **R1 — crawling against a three-day clock.** *Partially retired.* Research resolved the gate: crawling survives, but the sanctioned API is access-gated, so the free path is an HTML crawl with a one-request-per-package detail cost. The **fallback trigger is now settled** — if the detail route cannot show, within the first two working hours, throughput yielding roughly 200 packages with `uraian_pekerjaan` populated, abandon breadth-first and take a real slice plus curated anchors.
- **R2 — nothing exists on Google Cloud.** No project, no billing, no enabled APIs. Only a human can create one. Still the map's hardest prerequisite.
- **R3 — the agent has no cloud console.** The agent writes code and runs containers locally but cannot click through GCP. Every cloud action is a CLI command a human runs or a credential a human pastes.
- **R4 — defamation exposure.** Naming real vendors or officials as colluders inside a public, judged artifact is legally sensitive. See *Integrity and defamation stance*.
- **R5 — dated external facts.** The submission window, judging rubric, and product availability were read from primary sources on 15 Oct 2026 and can move. Re-check anything load-bearing before building on it.
- **R6 — a $300 budget.** The free trial gives **$300 over 90 days** and no more. Vertex AI, BigQuery, Model Armor, and Agent Search all bill, and an unbounded classification run over a large corpus can eat a meaningful share of it before the demo is even recorded.
- **R7 — the architecture now has a dependency with its own maintenance risk.** LPSE retrieval rests on a third-party open-source library rather than first-party access. Pin it, or vendor it.

## Decisions so far

- [SIRUP retrieval feasibility](issues/01-sirup-retrieval-feasibility.md): **AMBER.** The PRD is stale — SIRUP moved to `sirup.inaproc.id` and the INAPROC API is gated behind a formal letter and IP whitelisting, so the viable route is an HTML crawl with a per-package detail cost, or LKPP's open XLSX datasets. Fallback trigger settled.
- [LPSE / SPSE retrieval feasibility](issues/02-lpse-spse-retrieval-feasibility.md): **GREEN.** The PRD's "hardest" data is the easiest — the PyProc library already returns announcement, participants, evaluations, and winner, and ships as an MCP server. Unresolved: whether `id_rup` can be joined to `kode_lelang`.
- [JDIH price-cap retrieval feasibility](issues/03-jdih-price-cap-retrieval.md): **GREEN.** Current-year SSH exists for the exact demo region (Perbup Sukoharjo No. 2/2026), with provincial and national discovery routes. Unverified: PDF parseability and real table shape.
- [Google Cloud stack verification](issues/04-google-cloud-stack-verification.md): **the stack is buildable.** BigQuery Graph is GA, Model Armor natively scans PDFs for embedded injection, ADK deploys to Cloud Run. Product names in the PRD have drifted; new-account credit is $300 over 90 days.

## Not yet specified

- **Whether the "planning-to-tender" claim survives** — pending *Does id_rup join to kode_lelang?*. If it fails, the video's framing changes, not just its data.
- **Whether to adopt PyProc as the ingestion layer** — a maintained dependency is faster and better-tested than a bespoke crawler, but it complicates the story judges hear about what the team built.
- **Which real tender exhibits the red flags** — a high-bid winner, a repeated co-bidding group, or rival firms at one address. The retrieval path is now cheap; the finding is still outstanding.
- **Cost control** — $300 over 90 days is known, but the allocation is not: what gets capped, what happens at the cap, and whether the full-corpus classification pass is affordable at all.
- **Maps Places geocoding viability** — address-overlap detection is load-bearing in the syndicate graph and depends on an API that remains unpriced and unverified.
- **Model Armor integration depth** — a real pre-ingestion guard versus a scripted toggle that simulates one. Both demo; only one is a system.
- **Where data lives** — BigQuery-native versus a local store with BigQuery reserved for the graph.
- **PDF extraction reality** — whether the SSH documents parse cleanly enough to ground prices, or whether that claim needs to be narrowed.
- **The quality of `alasan_gugur`** — whether disqualification text is rich enough for a model to add anything over a keyword match, which decides if the highest-bid-winner detection is analysis or decoration.
- **Video production** — who narrates, what captures the Cloud Console proof shot, and how three minutes gets cut.
- **Deck content and ownership.**
- **Judge-reachable deployment** — public access, auth, quota, and what happens when a judge's request is the one that trips a limit.
- **Crawl politeness policy** — rate limits, robots.txt, and whether bulk-scraping government portals is defensible for a judged entry.
- **The adversarial Prosecutor/Defense loop** — genuine verification or a token sink. Its value at three days is unproven.
- **"Fresh project" compliance** — how the submission demonstrates the work happened inside the 7 Sept – 18 Oct window.

## Out of scope

Consciously beyond a submitted entry. Closed, never graduates.

- **AHU corporate enrichment dropzone (PRD Tier 2)** — director, commissioner, and notary extraction from uploaded deeds. Needs documents only auditors and journalists hold; cannot move a three-day submission.
- **Year-over-year budget inflation tracking** (`tahun_anggaran` deltas) — a real product feature, not a demo asset.
- **National-scale coverage** — the PRD's "three million rows a year" framing is the problem statement, not the build target.
- **Post-competition productization** — no hardening, no onboarding, no users beyond the judged demo.
- **Live e-commerce price scraping beyond grounding needs** — retail benchmarking earns its place only where the SSH grounding path visibly fails.
- **The `sirup.lkpp.go.id` domain and the PRD's API premise** — superseded by the INAPROC migration; retained only as historical context.
