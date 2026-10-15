# 22: Syndicate graph for one tender

**What to build:** The relationships between a tender's participants rendered as a graph, with the behavioural signals that make it worth looking at.

**Blocked by:** 21 (*LPSE execution view*)

**Status:** ready-for-agent

- [ ] The graph is built in BigQuery Graph over participants, vendors, tenders and the shared identifiers that link them.
- [ ] A **high-bid-winner** signal is raised where cheaper bidders failed evaluation and the winner sits near the HPS.
- [ ] A **cover-bidding** signal is raised where the same set of vendors repeatedly appears together across tenders.
- [ ] Vendor identity is clustered across masked NPWP prefixes and normalised name variants, so one company under two names is one node.
- [ ] Candidate shared-address clusters are surfaced as items to review and never as a finding of collusion.
- [ ] Address detection degrades to fuzzy matching rather than depending on an unpriced geocoding service, and says which method produced a cluster.
- [ ] The graph renders as a node-link view in the drawer, legible at 720p, and loads without a perceptible wait.
- [ ] Every signal carries its provenance, including the deterministic versus model-asserted distinction.
- [ ] Signals are covered by tests over a fixture tender set with known behaviour, including a clean case that raises nothing.
