# 20: Model Armor as a real pre-ingestion guard

**What to build:** A pre-ingestion security gate that inspects untrusted procurement text and uploaded documents before any model sees them, and that can be demonstrated on demand.

**Blocked by:** 18 (*Gemini normalisation and the taxonomy*); wayfinder ticket 08 (*Architecture lock*)

**Status:** ready-for-agent

- [ ] `spesifikasi_pekerjaan` text and any uploaded document are screened before reaching the model, and nothing the model receives bypasses the gate.
- [ ] A specimen carrying a hidden instruction to classify a package `NORMAL` is intercepted, and no classification is produced from the poisoned input.
- [ ] The block is recorded with what was intercepted, retrievable from the API and visible in the telemetry panel, rather than silently swallowed.
- [ ] The guard can be triggered on demand for a live demonstration.
- [ ] A clean input passes through and the pipeline continues unchanged.
- [ ] A guard error is recorded and surfaced explicitly and never defaults to "clean".
- [ ] Screening covers both prompt-side and response-side content, so a payload cannot reach the user through the model's answer.
- [ ] The gate's behaviour on a blocked input is covered by a test over a recorded poisoned specimen.
