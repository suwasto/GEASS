# JDIH price-cap retrieval feasibility

Labels: wayfinder:research
Type: research
Status: resolved
Blocked by: —

Related: 07, 08 — the grounding path in the architecture depends on whether these documents parse.

## Question

Are regional statutory price caps — Pergub, Perbup, and Perwali SSH & SBU documents — actually discoverable and parseable into structured `harga_satuan_maksimum` rows for the specific regions GEASS screens in its demo?

The PRD's Module 1 claims "neuro-symbolic price grounding" as its first headline innovation, and Capability 3 depends entirely on this corpus existing in usable form. Answer against primary sources: the actual `jdih.*.go.id` portals and the PDFs themselves.

- Which JDIH portals host SSH/SBU documents, and is there a search surface or only browsing?
- Are the documents machine-readable PDFs with a text layer, or scans requiring OCR? Test at least one real file rather than assuming.
- Do they contain the fields the PRD names: `kode_barang`, `uraian_barang`, `spesifikasi`, `satuan`, `harga_satuan_maksimum`? If the real table shape differs, describe what it actually is.
- **Coverage for the demo regions.** Specifically: Kabupaten Sukoharjo and Jawa Tengah, DKI Jakarta, and Jawa Timur. Which of these have a current-year SSH available?
- What is a workable extraction path, and what does it cost in time? The PRD routes this through Vertex AI Search as a RAG datastore — assess whether the documents are parseable enough for that to work without a bespoke extraction step.
- If a region's SSH is missing, what is the fallback for grounding that package's price — and does the demo narrative need to change accordingly?

## Deliverable

A verdict — **green**, **amber**, or **red** — the concrete list of retrievable SSH/SBU documents for the demo regions, the real table shape, and the extraction path with an honest time estimate.

## Answer

**Verdict: GREEN — current-year statutory price caps exist for the exact demo region — with one unverified parseability risk that a judge can see.**

**The demo region's current SSH is published.** [Peraturan Bupati Sukoharjo Nomor 2 Tahun 2026 tentang Standar Harga Satuan Tahun Anggaran 2026](https://jdih.sukoharjokab.go.id/produk/detail/14646) — the same `Kab. Sukoharjo` the PRD uses as its anchor case, for the same budget year the demo covers. Worth noting: BPK lists Perbup Sukoharjo 14/2025 (SSH TA 2026) as *Tidak Berlaku*, so the 2026 Perbup supersedes it. Cite the live one, not the one a search engine surfaces first.

**The provincial tier is also available.** [Peraturan Gubernur Jawa Tengah Nomor 20 Tahun 2025 tentang Standar Harga Satuan Pemerintah Daerah](https://jdih.jatengprov.go.id/inventarisasi-hukum/detail/pergub_20_th_2025), enacted 18 July 2025.

**Two retrieval surfaces, one of them national:**

- **Subject index, not one-off links:** `jdih.jatengprov.go.id/inventarisasi-hukum/subjek/standar-harga-satuan` enumerates standar-harga-satuan documents for the province. Provincial JDIH portals are searchable by subject, so this scales past a single hand-copied URL.
- **National aggregator:** `peraturan.bpk.go.id` indexes regional regulations nationally via `/Details/<id>` pages. This is the cheapest way to enumerate SSH documents across many regions at once, and it was how the Sukoharjo No. 14/2025 supersession above was detectable.

**Scope breadth is better than expected.** Tebo's Perbup 33/2025 covers SBU, SSH, HSPK, and ASB in one document — so a single regional regulation can carry several distinct price standards, which strengthens the grounding claim rather than requiring one document per benchmark type.

**Unverified, and this is the risk: parseability and table shape.** Whether these PDFs carry a text layer or are scans requiring OCR was not established. Neither was the real column structure against the PRD's assumed `kode_barang`, `uraian_barang`, `spesifikasi`, `satuan`, `harga_satuan_maksimum`. The PRD routes extraction through a Vertex AI Search datastore; if the documents are scans or the table is laid out per-item with merged cells, that path will silently produce garbage. **Test one real PDF before the grounding claim goes in the video.**

**If a region's SSH is missing:** fall back to the provincial SSH, or to the BPK copy of the regional one, and say so in the UI rather than silently grounding against nothing.
