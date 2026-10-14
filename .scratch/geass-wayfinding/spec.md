# GEASS evidence-backed hackathon demo specification

Status: ready-for-agent
Label: ready-for-agent
Version: 1
Date: 2026-10-14 (Asia/Jakarta)
Parent: [Resolved GEASS wayfinder map](map.md)

This is an implementation specification, not an implementation ticket or permission to provision cloud resources. Work starts with the readiness gate. The map remains the index of architecture decisions; this specification defines observable product behavior.

## Problem Statement

Journalists, civic watchdogs, and inspectors cannot manually compare public procurement plans, regional price standards, and tender outcomes at scale. The available records differ in completeness and provenance. A confident model explanation, similar vendor names, or a large planning ceiling can mislead users if presented as evidence of wrongdoing.

GEASS must make a small set of authentic, traceable procurement leads understandable and reviewable without converting missing information into accusations. Public users need the evidence and limitations behind a reviewed finding, while operators need controlled analysis and reviewers need authority over what becomes public.

## Solution

Build a browser demo for one region and budget year, chosen through a permitted-source sample. An operator imports controlled evidence captures and runs bounded, resumable analysis. A reviewer examines source-backed risk signals and counterevidence, then approves an exact case version for publication. Anonymous users browse approved cases, inspect applicable benchmark comparisons and available tender/vendor observations, and download Markdown draft dossiers.

The first successful story follows one authentic planning package through a defensible price comparison and a verified lifecycle link where the records support it. Unsupported analysis visibly abstains. A reduced planning-only demonstration is possible if execution data is inaccessible, but it does not satisfy the full lifecycle demonstration and requires an explicit scope decision.

### Product surfaces

- **Public radar:** paginated dense table, region/agency/signal filters, evidence coverage and clear empty/error states. Only approved projections are listed.
- **Case investigation:** source-backed planning detail, quantity/benchmark comparison, supporting and contradicting evidence, lifecycle coverage, bounded vendor graph and equivalent accessible table.
- **Reviewer workspace:** authenticated private drafts, evidence references, analysis limits and review decisions on exact versions. Operator controls are separately authorized.
- **Draft downloads:** PPID information-request draft and APIP/BPK risk brief, clearly marked for human completion and review.
- **Demo inspector:** sanitized execution outcomes and trace references; cloud-console evidence is recorded separately without exposing console access or raw traces publicly.

## User Stories

1. As a public reader, I want to browse approved planning packages without logging in, so that procurement oversight is accessible.
2. As a public reader, I want pagination and region, agency, and risk filters, so that I can find relevant local cases without loading national data.
3. As a public reader, I want pagu labeled as a planning ceiling, so that I do not mistake it for actual spending.
4. As a public reader, I want source links, observation dates, and field-coverage information, so that I can assess what the case actually establishes.
5. As a public reader, I want real evidence and synthetic demonstrations clearly distinguished, so that I do not mistake a test fixture for a real allegation.
6. As an investigator, I want the package title compared with available descriptions and specifications, so that vague wording can be examined with source evidence.
7. As an investigator, I want mandate questions supported by mandate references or marked unresolved, so that a model's intuition is not treated as institutional authority.
8. As an investigator, I want a validated quantity and comparable benchmark shown together, so that I can reproduce a unit-price comparison.
9. As an investigator, I want benchmark year, jurisdiction, unit, specification, and applicability displayed, so that unrelated prices cannot silently support a markup claim.
10. As an investigator, I want bundled or ambiguous quantities to produce insufficient evidence, so that GEASS does not invent unit prices.
11. As an investigator, I want multiple risk signals and their individual evidence states, so that one unsupported check does not obscure a supported observation.
12. As an investigator, I want threshold comparisons tied to category and effective rules, so that near-threshold values are not automatically classified as illegal splitting.
13. As an investigator, I want a source-backed planning-to-execution relation, so that I can follow the actual lifecycle rather than a title-similarity guess.
14. As an investigator, I want unavailable execution records distinguished from absent tenders, so that gaps in source access are not interpreted as facts.
15. As an investigator, I want registered participants, submitted bids, evaluations, and winners distinguished, so that co-bidding and high-bid observations use the right denominator.
16. As an investigator, I want graph edge types, provenance, and coverage windows explained, so that connections do not imply proven affiliation.
17. As an investigator, I want shared addresses, masked identifiers, and fuzzy names treated as candidate associations, so that unrelated vendors are not merged automatically.
18. As a reviewer, I want supporting evidence, counterevidence, and unresolved objections together, so that I can challenge a proposed finding.
19. As a reviewer, I want AI debate to remain advisory, so that publication is my decision rather than an agent action.
20. As a reviewer, I want to approve or reject an exact evidence and analysis version, so that later changes cannot inherit stale approval.
21. As a reviewer, I want to withdraw a published case, so that the public view and downloadable artifacts cease being available when appropriate.
22. As an operator, I want to import permitted, provenance-backed captures with validation feedback, so that invalid or unauthorized inputs do not enter analysis.
23. As an operator, I want manually triggered bounded batches and visible stage status, so that analysis stays within execution and spending limits.
24. As an operator, I want interrupted work to resume from committed stages without duplication, so that retries preserve results and review history.
25. As an operator, I want failed, skipped, or unsupported security screening quarantined, so that HTTP success or model confidence cannot bypass the input boundary.
26. As a public reader, I want a downloadable draft information request with source identifiers and evidence limits, so that I can prepare a request without GEASS contacting anyone.
27. As an inspector, I want a downloadable risk brief containing calculations and counterevidence, so that I can prioritize further verification.
28. As a keyboard or assistive-technology user, I want the table, detail, graph alternative, review actions, and downloads accessible, so that the investigation does not depend on pointer interaction or color.
29. As a judge, I want an authentic deployed investigation and safe cloud execution evidence, so that I can distinguish working integration from a mockup.
30. As the project owner, I want readiness inputs and measured evaluation boundaries recorded, so that the demo does not claim national accuracy or production readiness.

## Implementation Decisions

### Architecture and ownership

Honor the six accepted ADRs indexed by the map. Google Cloud is fixed: Python/FastAPI, Google ADK, Vertex AI, BigQuery, and Cloud Run. React/TypeScript with Vite is served by the same web/API deployment. Analysis runs as a manually triggered Cloud Run Job; browser reads never initiate model inference.

Use private Cloud Storage for immutable source captures and artifacts, BigQuery for analytical observations and SQL-derived signals/edges, and the plan's Firestore recommendation for durable run/review state and approved case pointers. Confirm this operational integration, regional compatibility, and cost in readiness. No separate graph database, GQL reservation, autonomous loop, or MCP server is required for the initial demo.

Logical modules are evidence ingestion, canonical observations, benchmark retrieval/comparison, bounded assessment orchestration, graph projection, review/publication, dossier generation, and browser/API presentation. Reuse one evidence-reference contract across them; do not duplicate quantity parsing, citation validation, or review authorization in individual agent roles.

### Readiness gate

Before scaffolding the application, record the selected region/year, permitted sample and coverage manifest, deadline, project/region, cloud access, billing authorization, maximum spend, operator/reviewer identities, supported model/version and smoke-test evidence. Confirm official competition requirements before using the PRD's claimed judging weights or timing as constraints. No credential values belong in documents, fixtures, logs, or browser assets.

Use at least one authentic planning record, one applicable SSH comparison, and one verified execution link with sufficient participant/bid/evaluation fields for the intended lifecycle demonstration. Include ordinary and missing-data cases. Dataset size follows permitted coverage and limits; 5,000 rows and a four-day delivery are not acceptance promises.

Model selection is an execution gate, not the PRD's hardcoded Gemini 2.5 choice. The research reports October 20, 2026 retirement for both named models; recheck lifecycle and select a supported GA model before running. Validate structured output, retrieval/tool compatibility, quotas, IAM, screening status handling, and checkpoint durability in the actual project.

When permitted API access is unavailable, a curated provenance-backed snapshot is acceptable. When execution coverage is unavailable, display that limitation and obtain a scope decision for any reduced real-data demo. Synthetic fixtures demonstrate software behavior only and cannot establish a real vendor ring or fulfill authentic lifecycle acceptance.

### Evidence and record contracts

Every capture has source URL/portal, retrieval time, content checksum, source revision, permitted-access basis, original-object reference, parser version and field coverage. Extracted PDF evidence retains page/row locators. Source bytes and past observations are preserved; corrections create new observations.

Planning identity preserves external RUP identifiers as strings with source scope and fiscal year. Tender identity combines portal and external tender identifier. Preserve leading zeros. Planning-to-execution relations are zero-to-many, versioned observations with verified, candidate or unavailable state. Only verified links support a combined finding.

Amounts use decimal IDR arithmetic. API amounts are decimal strings, not floating-point JSON numbers; missing amounts remain null. Dates/times use ISO-8601 with explicit offsets; the UI displays observation dates in Asia/Jakarta. Required identifiers are validated, unknown source fields remain unknown, and missing values never become invented zeros.

A benchmark records the legal instrument/version, approved status, jurisdiction, fiscal year/effective period, page/row, specification, unit, decimal price and applicable tax/logistics notes. A source standard is not automatically a legal maximum; its operative applicability must be established. Retail comparisons are deferred.

A signal records rule/version, supporting observations, source references, deterministic calculation when applicable, counterevidence and limitations. Its evidence status is supported, insufficient evidence or not assessed. Taxonomy labels are independent of evidence status and may coexist. NORMAL describes only sufficiently evidenced checks performed, never missing input.

### Analysis behavior

Screen and validate untrusted source content before model stages. Persist individual scan/filter outcomes; failed, skipped, incomplete and unsupported outcomes quarantine the work item. Treat document text as data, separate it from instructions, use narrow allowlisted tools, and reject arbitrary SQL or source-supplied tool destinations. Model Armor is one detector rather than proof of complete protection.

Structured extraction proposes item, quantity, unit and relevant source spans. Validate finite positive numeric quantities and comparable units before computation. Bundled `1 Paket`, mixed items, unclear quantity, inconsistent specification, wrong year/jurisdiction or unknown applicability disables the unit-price comparison. The model never performs authoritative arithmetic.

For eligible comparisons, implied unit price equals planning pagu divided by validated comparable quantity. Price delta and ratio are calculated deterministically against the applicable benchmark. Display assumptions; a large delta alone is a lead, not proven overpayment. Signal escalation thresholds must be versioned and calibrated against a hand-reviewed set before publication, rather than inferred from an LLM's confidence.

Title/specification, mandate and tailored-spec signals require cited observations. Missing mandate authority yields an unresolved review question. Split-package candidates require comparable scope, category, method, period and effective rules; closeness to a threshold alone cannot establish intent.

ADK runs explicit bounded stages: normalization, grounded planning assessment, deterministic signal/graph retrieval, advisory prosecutor/defense review, and structured result validation. Persist stage outputs and completion state outside memory. Keep concise evidence-backed rationale, not private chain-of-thought. No component may authorize publication on the reviewer's behalf.

### Runs and recovery

A work key combines source revision, case identity, analysis version and selected model/version. A repeated trigger returns the existing work item or explicitly resumes a failed stage; it does not create duplicate findings. Use conditional stage claims and durable completion commits so concurrent triggers cannot both publish completion. Persist attempts, execution limits and safe error reasons.

Run state is queued, running, completed, failed or quarantined. Completion means all required stage outputs passed validation; an insufficient-evidence assessment can be a completed result but cannot support its unavailable signal. Security quarantine is never equivalent to completion. Resume only committed-safe work, verify source/config identity on retry, and preserve all review history.

Enforce bounded dataset scope, retries, wall time, model calls, job concurrency and BigQuery bytes scanned. Budget alerts do not themselves impose a hard cap. Values are execution inputs established at readiness; the spec invents no budget, response-time target or national capacity guarantee.

### Vendor graph

Generate bounded SQL projections for observed vendor/tender relationships. Each edge records type, evidence, observation window and count/denominator. Distinguish actual bid submission from registration; absent evaluation records disable disqualification-based claims. High-bid signals require known bid amounts, evaluation states, reasons and winner records.

Shared address/name/NPWP observations create candidate links, not identity merges or beneficial ownership. No automatic fuzzy entity merge occurs in the first demo. UI graphs include legends, coverage limits, truncation indicators, and an equivalent textual/table representation. A graph does not establish collusion.

### API behavior

Contracts below describe required operations; exact route spelling is an implementation detail. Use one versioned HTTP/JSON API with server-side validation, bounded pagination/graph responses and consistent safe errors. No general SQL endpoint or arbitrary URL-fetch endpoint exists.

| Surface | Operation and observable contract |
| --- | --- |
| Public cases | List approved current projections with allowed region/agency/signal filters, stable ordering, bounded page size and continuation token; no matches returns an empty page |
| Public case detail | Return the approved version with public planning facts, coverage, signal explanations, benchmark assumptions and supporting public locators; unknown, draft-only and withdrawn cases return the same non-disclosing not-found response |
| Public graph | Return only the graph approved with that case version, including evidence edges and limits; unavailable coverage is distinct from a complete graph with no matching edges |
| Public dossier download | Return UTF-8 Markdown as a draft attachment tied to the approved case version; stale, draft or withdrawn versions cannot bypass access checks through artifact URLs |
| Operator import/analysis | Allowlisted operator only; validate controlled capture references and limits, return an asynchronous work identity, and reuse the work key on duplicate triggers |
| Private run/draft reads | Authorized operator/reviewer only; expose stage status, safe failures and source-backed draft assessments, never secrets or private model reasoning |
| Review decision | Allowlisted reviewer only; require exact draft/evidence version and requested approve/reject decision; stale versions produce a conflict, invalid incomplete/quarantined assessments cannot be approved |
| Withdrawal | Allowlisted reviewer only; invalidate public case and download access, preserve private audit history; repeat withdrawal is safe |

Unauthenticated protected requests are unauthorized; authenticated identities lacking the relevant role are forbidden. Malformed input is a validation error; stale versions are a conflict; external failures use safe retryable/unavailable errors. Response messages never include raw stack traces, credentials or private document content.

### Publication and authorization

Use Google identity authentication and a server-side allowlist for the small operator/reviewer group; validate issuer, audience and expiry in the selected integration. Authentication does not imply reviewer permission. Separate web and analysis identities, use least-privilege service access, and protect cookie-backed mutations against CSRF if that integration is chosen.

Review states are draft, approved, rejected and withdrawn. Approval binds reviewer identity/time, analysis version, source-evidence versions and the public projection version. New evidence or analysis creates a new draft, never an inherited approval. The prior approved snapshot remains identifiable until explicit supersession or withdrawal.

Public reads use a sanitized approved projection, never the raw analytical/private document store. Do not expose masked tax data, raw identity enrichment, unreviewed rationale, draft documents, operational controls, or arbitrary object access. Check publication state on downloads and use a cache policy that permits immediate withdrawal without waiting for a CDN expiry. Already downloaded copies cannot be recalled; the guarantee covers subsequent server access.

### Dossiers, presentation and telemetry

Provide PPID request and APIP/BPK brief as downloadable Markdown drafts. Include the reviewed version, planning/tender identifiers where known, source locators, calculations, assumptions, counterevidence, unresolved issues and draft status. Recipient/sender fields remain human-completed where not evidenced; nothing is sent or filed automatically. Validate legal/template references before representing the wording as appropriate for public use.

Indonesian is the default demo UI and dossier language; use localized labels and IDR formatting. Show facts, AI-supported interpretation and evidence gaps distinctly. The initial visual direction follows the PRD's dense dark table and forensic detail panel; detailed visual design is not locked by this spec. Meet keyboard navigation, visible focus, readable contrast, labeled controls and a graph alternative; never communicate risk by color alone. Escape all source/model text and restrict citation destinations to permitted web links.

Trace run/stage identity, safe outcomes, durations, selected model and rule versions, and budget-relevant usage. Exclude credentials, private personal/source content and private chain-of-thought. A public demo inspector exposes only sanitized summaries; cloud-console captures remain separate proof. Record actual deployed revision and successful API/query/model/security evidence, not just screenshots of configured services.

## Testing Decisions

There is no existing application or test suite to reuse. Use the previously agreed user-flow and API behavior boundaries as the highest test seams; add focused deterministic calculation tests only where failure cases cannot be expressed economically through the public contracts. Do not test internal agent names, file layout, component implementation or prompt wording.

- **Primary acceptance seam:** browser investigation against the real API: approved radar → source-backed detail → benchmark/counterevidence → available graph → draft download. Test a real deployed case separately from deterministic local fixtures.
- **Protected API seam:** import/trigger/recovery and review/publication operations exercise authorization, idempotency, version checks and public redaction. Anonymous/public reads and artifact retrieval are part of the same boundary.
- **Deterministic evidence seam:** known quantities, prices, units and source versions test exact decimal arithmetic, comparability and effective-dated rules. Fixed model/retrieval responses isolate these checks from inference variation.
- **Live integration evidence:** actual model structured output/retrieval, screening verdict enforcement, BigQuery SQL, storage/state recovery and Cloud Run deployment. A mock response is not proof of cloud integration.

| Acceptance scenario | Required result |
| --- | --- |
| Valid known quantity and applicable SSH page | Reproducible exact calculation, source reference and assumptions |
| Bundle, mixed items, missing/zero quantity, wrong unit/year/jurisdiction or draft standard | Unsupported comparison abstains and names the missing condition |
| Missing description, mandate authority, evaluation or bids | Only dependent checks disabled; missing is not NORMAL, a losing bidder, or evidence of no tender |
| Valid emergency/logistics exception or cheaper bidder validly disqualified | Counterevidence retained; no unsupported accusation |
| Effective-dated category threshold cases | Goods/other-service, construction and consultancy rules distinguished; no automatic intent finding |
| Similar names, masked identifiers or shared address | Candidate association only; distinct source identities retained |
| Changed RUP relation or multiple executions | Observed history and zero-to-many relation preserved |
| Invalid structured model result or unsupported citation | Bounded validation failure or insufficient evidence; no publishable unsupported signal |
| Indonesian/English injection, encoded content, oversized/unsupported input, skipped scan or timeout | Enforced quarantine/error disposition and no tool escape or publication |
| Interruption after stage commit, repeated/concurrent trigger | Safe recovery without duplicate findings or overwritten review |
| Anonymous or unauthorized review, stale approval, raw-object access | Request blocked with safe response; private data absent from public surface |
| Evidence changes after approval | New draft requires review; old approval cannot authorize new output |
| Approved case withdrawn and old dossier URL requested | Subsequent public case and artifact retrieval denied, audit history retained |
| Keyboard use, narrow viewport, graph unavailable and empty filters | Readable navigation and explicit non-misleading states |

Use a small hand-reviewed authentic evaluation set plus clearly synthetic edge fixtures. Record source coverage, model/rule versions, measured latency/cost and failures. Precision/recall applies only to that set's explicit labels; citations and model confidence are not calibrated anomaly probabilities. Set signal calibration targets before publishing those labels. Do not claim national accuracy or production readiness from a demo.

## Out of Scope

This specification does not create application scaffolding, production code, cloud resources, deployment, implementation tickets or external GitHub issues. Initial demo scope excludes nationwide ingestion, continuous monitoring, citizen/AHU uploads, geocoding, live retail/e-Katalog benchmarks, GQL reservations, a separate graph database, PDF output, automated message sending/filing, criminal accusations, broad reviewer onboarding and production SLAs.

## Further Notes

- Authority: the user's three architecture rounds, the six accepted ADRs, the domain glossary and the resolved map. The PRD supplies the product vision; accepted decisions and documented feasibility corrections govern the demo.
- [Sequenced build plan](../../docs/geass-build-plan.md) supplies milestone ordering. Slice implementation tickets from this spec only when requested, beginning with readiness/source evidence, then one package read, then one SSH comparison.
- [Cloud research](../../docs/research/google-cloud-feasibility.md) and [procurement research](../../docs/research/procurement-data-feasibility.md) cite official sources and list verification limits. No live portal/API, Google Cloud project, cost or runtime suitability was proved during planning.
- Readiness inputs remain open execution prerequisites: budget/billing authorization, deadline, project/region, source reuse/access, authentic sample coverage, reviewer/operator identities, model choice and calibrated signal thresholds. They are not hidden assumptions or permission to spend.
- If readiness evidence changes an accepted boundary, reopen the map with a precise decision question before implementing the affected feature. Routine implementation details can be settled within their ticket without reopening the product scope.
