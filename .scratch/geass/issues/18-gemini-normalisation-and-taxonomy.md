# 18: Gemini normalisation and the taxonomy

**What to build:** Each crawled package normalised to its true underlying item and classified into the fixed five-class taxonomy with Indonesian reasoning — with the model structurally unable to contribute a number that reaches a user.

**Blocked by:** 17 (*Per-package detail crawl*); wayfinder ticket 08 (*Architecture lock*), which owns the agent topology

**Status:** ready-for-agent

- [ ] The wrapper title is normalised to an underlying item, a quantity candidate and a unit candidate, each schema-validated on arrival.
- [ ] The classification is one of `ABSURD`, `INDICATED MARKUP`, `SPECIFICATION LOCK`, `PECAH PAKET`, `NORMAL` — and nothing else can be stored.
- [ ] Indonesian reasoning accompanies every classification and is never empty.
- [ ] A validation failure is recorded as a failure for that package and never coerced into a valid-looking record.
- [ ] A deterministic pre-filter narrows the corpus to candidate anomalies before any model call.
- [ ] A hard model-call cap fails the run loudly rather than spending past its threshold.
- [ ] Model tiering is explicit: the cheap model for extraction and normalisation, the stronger model only where classification needs it.
- [ ] A test with a stubbed model returning numeric-looking claims proves that no IDR figure in any API response changes.
- [ ] Only the fields the model needs are sent, so unrelated text cannot steer a classification.
- [ ] The badge and its reasoning render on the radar row and in the drawer.
