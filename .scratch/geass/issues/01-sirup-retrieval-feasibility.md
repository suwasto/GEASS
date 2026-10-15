# SIRUP retrieval feasibility

Labels: wayfinder:research
Type: research
Status: resolved
Blocked by: —

Related: 07 — the demo narrative can only commit to cases this ticket proves retrievable.

## Question

Can GEASS obtain real SIRUP package data, at the fidelity Module 1 needs, inside the hackathon window — and at what volume?

The map has already committed to a **live, breadth-first crawl** (risk R1). This ticket decides whether that commitment is safe to build on, so it is the gate that runs before any crawl code is written.

Answer against primary sources only: LKPP's own portals, INAPROC open data, official API docs, and the live pages themselves. Do not trust secondary write-ups.

- What public retrieval surfaces exist today — SIRUP public JSON endpoints, INAPROC open data, any documented API, or HTML-only package detail pages?
- Of the eleven parameters the PRD's Module 1 depends on, which are actually exposed: `id_rup`, `nama_paket`, `klpd`/`pemilik`, `satker`, `lokasi_pekerjaan`, `total_pagu`, `uraian_pekerjaan`, `spesifikasi_pekerjaan`, `volume_pekerjaan`, `metode_pemilihan`, `jenis_pengadaan`, `tahun_anggaran`?
- Which of those live only on the per-package HTML detail page rather than in any list endpoint — and therefore demand one request per package?
- What are the actual rate limits, robots.txt rules, and terms of use?
- Are current-year planning rows reachable, and is historical data exposed at all?
- **Achievable volume.** Given the constraints above, how many usable rows can realistically be retrieved in a few hours of crawling? Give a number and the assumptions behind it.
- **Are the PRD's anchor packages real?** Verify that `65174830`, `64154392`, and `65028950` are actually retrievable and that their quoted figures (IDR 200,000,000 flowers; IDR 198,150,000 Sky View; IDR 188,000,000 DPRD reception) match what the live pages say.

## Deliverable

A verdict — **green** (crawl as planned), **amber** (crawl but scope it), or **red** (abandon and take the fallback) — plus the concrete retrieval recipe and the achievable row count. The verdict directly settles the *Crawl fallback trigger* patch currently sitting in the map's **Not yet specified**.

## Answer

**Verdict: AMBER — crawling survives, but not by the route the PRD assumes, and not through the sanctioned API on this timeline.**

**The PRD is stale on two counts.** `sirup.lkpp.go.id` has been retired; SIRUP now lives at **`sirup.inaproc.id`** (moved 1 Dec 2025). And LKPP has since published a documented **INAPROC API Gateway** at `data.inaproc.id`. The plan's premise — "SIRUP public JSON endpoints" — must be rewritten before any crawl code is written. [Source: migration guide](https://data.inaproc.id/docs/dokumentasi/guides/migration-from-isb)

**Three routes exist; only two are open to us.**

1. **INAPROC API Gateway — blocked on bureaucracy.** A real, versioned REST surface covering exactly what Module 1 needs: `/api/v1/rup/paket-penyedia`, `/api/v1/rup/paket-swakelola`, `/api/v1/rup/master-satker`, `/api/v1/rup/paket-anggaran-penyedia`, `/api/v1/rup/program-master`. But access requires an **INAPROC account, the `Data Integrator` role, a formal access-request letter (*Surat Permohonan Akses*) sent to LKPP, admin approval, and a whitelisted public IP**, after which a JWT is generated in the Developer Portal. That queue is measured in days, not hours, and cannot be assumed inside a three-day window. [Source: API specification](https://data.inaproc.id/docs/spesifikasi-api)
2. **SIRUP public web UI (`sirup.inaproc.id`) — the realistic path.** Public recap and package-detail pages remain browsable, so an HTML crawl is what we actually have. Expect **one request per package** for `uraian_pekerjaan`, `spesifikasi_pekerjaan`, and `volume_pekerjaan`, because those fields surface on the detail page rather than in any list view. Per-package request cost, not row count, is the real budget.
3. **LKPP open data (`data.lkpp.go.id/ro/dataset/`).** XLSX exports of SIRUP — "Nilai Paket RUP yang Terumumkan ... berdasarkan Kementerian/Lembaga/Pemerintah Daerah." No onboarding, bulk-shaped, weakest field granularity: a cheap way to seed volume alongside a targeted detail crawl.

**Rate limits.** Legacy endpoints cap at 100 requests/minute; v1 query endpoints are documented only as "per data source capacity," which is not a guarantee. Design for ~1 request/second.

**Achievable volume: not established here, deliberately.** This verdict rests on route selection, not throughput. List-level recap or XLSX retrieval reaches thousands of rows cheaply; the detail fields that Capability 1 and Capability 3 depend on are the expensive part. Sizing them is *Verify the PRD's anchor anomalies*' job.

**Anchor packages unverified.** `65174830`, `64154392`, and `65028950` could not be confirmed. The PRD cites them with no retrieval method, and the retired domain makes them unverifiable from the PRD alone. Each must be re-checked against the live UI before it carries any part of the demo.

**Fallback trigger — graduated out of the fog and settled here.** If the detail-page route cannot demonstrate, within the first two working hours, throughput that yields roughly 200 verified packages with `uraian_pekerjaan` populated, abandon breadth-first crawling and switch to a real slice plus curated anchors. The trigger is a technical consequence of the constraints above, not a preference; the team may move the threshold, but the trigger should exist. This clears the *Crawl fallback trigger* patch from the map's **Not yet specified**.

**Net effect on risk R1.** Breadth-first crawling survives, but it is not a "just crawl it" operation. The free path is HTML scraping with a per-package detail cost; the cheap-volume path carries weaker fields. That cost is what the three-day clock has to absorb.
