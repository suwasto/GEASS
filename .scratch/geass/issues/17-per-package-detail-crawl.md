# 17: Per-package detail crawl

**What to build:** The fields that reveal what was actually bought — retrieved one package at a time under a bounded, polite budget, with the throughput evidence that settles the crawl fallback trigger.

**Blocked by:** 16 (*Real SIRUP rows on the radar*)

**Status:** ready-for-agent

- [ ] `uraian_pekerjaan`, `spesifikasi_pekerjaan`, `volume_pekerjaan`, `metode_pemilihan` and `jenis_pengadaan` retrieved per package from the package-detail route.
- [ ] The crawl respects a configured inter-request delay of roughly one second, identifies itself honestly, and honours a maximum request budget per run.
- [ ] The run reports throughput and field completeness — how many packages carry `uraian_pekerjaan` — after the first two working hours of crawling, so the fallback trigger is settled on a number rather than a feeling.
- [ ] Parsers are pure functions from a raw payload to a typed record, tested directly against the specimens from ticket 14.
- [ ] The detail text is displayed beside the wrapper `nama_paket` for the same package, so concealment by generic naming is readable in one line.
- [ ] A non-200 or malformed response is recorded as a failure for that package and never written as an empty record.
- [ ] Firing the fallback trigger is a configuration change rather than a code change, and the reduced-scope run is demonstrably still a complete path.
- [ ] A package whose detail was never successfully retrieved is distinguished from one whose detail is genuinely absent.
