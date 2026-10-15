# 14: Fixture corpus and offline harness

**What to build:** A committed specimen corpus covering all three external sources, plus a test entry point that runs the parsers and the service with no network access — so every later slice can be built and verified without the live sources and without spending cloud credit.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] Raw specimens captured from each source and committed alongside the code: a SIRUP recap or list payload for one region and budget year; package-detail payloads for at least three packages carrying `uraian_pekerjaan`, `spesifikasi_pekerjaan` and `volume_pekerjaan`; the current Sukoharjo SSH regulation exactly as published; and one real LPSE tender carrying participants, evaluations, `alasan_gugur` and a winner.
- [ ] Each specimen records where it came from, when it was retrieved, and which request produced it.
- [ ] Specimens are trimmed to the smallest payload that still exercises the fields the product reads, and the committed total stays small enough to live in a public repository.
- [ ] At least three distinct package specimens exist, so parsers are exercised against variation rather than one happy page.
- [ ] The SSH specimen carries a recorded note on whether it has a text layer or is a scan.
- [ ] No specimen contains credentials, tokens, whitelisted IPs, or anything beyond what the source already publishes.
- [ ] A test entry point runs the whole suite with network access unavailable and passes.
- [ ] The corpus is documented well enough that a later slice can add a specimen without reverse-engineering the convention.
