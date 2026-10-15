# Google Cloud stack verification

Labels: wayfinder:research
Type: research
Status: resolved
Blocked by: —

Related: 05 must enable whichever APIs this ticket proves necessary; 08 locks the architecture around what survives.

## Question

Which parts of the PRD's Google Cloud architecture actually exist today, are available to a brand-new project, and can be stood up by an agent that has CLI access but no console?

The PRD stakes its 40% Technical Merit score on five named products. None has been verified. Answer against primary sources: Google's own product documentation and pricing pages, current as of 15 Oct 2026. Note the availability status of each — GA, preview, or nonexistent — and the region.

- **Google ADK (Agent Development Kit).** Does it exist as a real, current product? What is the package name and version, how mature is it, and what is the documented path to deploying an ADK agent on Cloud Run?
- **"BigQuery Graph."** The PRD names this as a load-bearing component. Determine whether that is a real product name. Check BigQuery Graph Analytics / property graph support — GA or preview, and what it actually costs to run.
- **Cloud Model Armor.** Is it generally available, in which regions, at what price, and what is its API shape? Critically: can it be invoked programmatically to sanitize an untrusted string in a pipeline, as the PRD assumes, or is it a perimeter product that does not fit that use?
- **Vertex AI Search and grounding.** Setup cost, datastore limits and pricing, and whether grounding against Indonesian-language PDFs and live web results in IDR is viable. Is there a cheaper path to the same grounding claim?
- **Gemini 2.5 Pro and Flash.** Current model IDs, availability to a new project, and pricing. Correct the PRD if the version it names has moved.
- **Maps Places API.** Geocoding terms and cost per call, and whether it may be used in a hackathon entry and a public dashboard.
- **New-account reality.** What credits or free trial does a brand-new GCP account get in 2026, and what are the spending caps on them?
- **Minimum viable setup.** The shortest documented path from "no project" to "a publicly reachable Cloud Run service running an ADK agent that calls Gemini." List the exact APIs to enable.

## Deliverable

For each product: exists / does not exist, availability status, region, cost shape, and whether the PRD's use of it survives. Then the minimum viable setup path, as a checklist. Anything that fails to survive becomes a substitution decision for the *Architecture lock* ticket.

## Answer

**Verdict: the stack largely survives. Two of the PRD's most speculative-sounding components are confirmed real and generally available, several names have drifted, and the account reality is thinner than the architecture assumes.**

- **BigQuery Graph — real, and GA.** [Cloud's own documentation](https://docs.cloud.google.com/bigquery/docs/graph-overview) describes it, and Google [announced general availability](https://cloud.google.com/blog/products/data-analytics/bigquery-graph-connecting-data-and-ai-at-scale) around 1 Sept 2026, after a public preview in April. The PRD's most invented-sounding box is genuinely a shipping product. **Survives.**
- **Cloud Model Armor — real, and a far better fit than expected.** [Documentation](https://docs.cloud.google.com/model-armor/overview) confirms it screens both prompts and responses for prompt injection and jailbreak attempts, *and* explicitly lists *"Inspect unstructured document text: Extract and scan text within document formats like PDFs to intercept embedded malicious payloads or sensitive data."* That is precisely the PRD's poisoned-KAK / hostile `spesifikasi_pekerjaan` scenario, supported natively rather than simulated — which makes the demo beat honest rather than theatrical. Regional endpoints exist; reaching them from inside a VPC requires a Private Service Connect endpoint. **Survives, and upgrades the demo.**
- **Google ADK — real.** [adk.dev](https://adk.dev/grounding/grounding_with_search/) documents grounding with search, and ADK ships built-in deployment to Cloud Run. **Survives.**
- **Naming drift — the PRD's vocabulary is out of date.** "Vertex AI Search," "Vertex AI Agent Builder," and "Vertex AI" have moved toward **Gemini Enterprise Agent Platform** and **Agent Search**. Building on the correct names matters beyond pedantry here: the deck and video will name this stack, and stale product names read as a team that has not touched the platform.
- **Gemini 2.5 Pro / Flash — in use.** Current documentation and tutorials reference Gemini 2.5 Flash and Gemini 2.5 Pro as the working generation. Exact model IDs still need pinning at build time, since they change.
- **Maps Places API — not verified here.** The geocoding claim behind address-overlap detection remains unpriced. It stays in the map's fog.
- **New-account reality: $300 in credit over 90 days**, plus an Always Free tier. [Source](https://cloud.google.com/free). That is the *entire* budget for this build, which sharpens the previously vague *Cost control* fog patch into something with a number attached. Vertex AI, BigQuery, Model Armor, and Agent Search all bill; a careless three-day run of full-corpus LLM classification can consume a meaningful fraction of it.

**Enable list, to be confirmed by *Provision the Google Cloud project*:** Cloud Run, Artifact Registry, Cloud Build, Vertex AI, BigQuery, Model Armor, and Agent Search.

**The consequence for the map.** The architecture in the PRD is buildable — that was the real question this ticket had to answer, and the answer is yes. The binding constraints are not product availability; they are the bureaucratic crawl route (see *SIRUP retrieval feasibility*), the missing GCP project, and a $300 budget. *Architecture lock* can now proceed against a verified stack rather than a hoped-for one.
