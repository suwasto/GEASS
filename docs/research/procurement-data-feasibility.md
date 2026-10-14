# Procurement data feasibility

Research date: 2026-10-14 (Asia/Jakarta). Scope: planning evidence, not an implemented or tested connector.

## Findings that change the PRD

1. **Public source existence is confirmed; universal machine-readable completeness is not.** LKPP's public-information register identifies SIRUP as its RUP publication service and links the current `sirup.inaproc.id` domain. It separately identifies `data.inaproc.id/profil-pengadaan` as the national procurement profile. Neither page documents the PRD's claimed public JSON contract, rate limits, licensing, or universal detailed-field coverage. Treat PRD field names as GEASS's proposed canonical schema until mapped against captured source samples. [LKPP SIRUP register](https://ppid.lkpp.go.id/information/public/136/sistem-informasi-rencana-umum-pengadaan), [national procurement register](https://ppid.lkpp.go.id/information/public/203/portal-pengadaan-nasional).

2. **An official published RUP table exists, but does not establish a detailed national schema.** LKPP publishes a 2025 RUP PDF containing names, pagu, selection methods, funding, RUP codes and timing. This is useful evidence for a curated import fallback; it does not prove that descriptions, specifications and usable quantities are available for every row. [LKPP published RUP PDF](https://ppid.lkpp.go.id/admin/uploads/dip_file/I.1.%20rencana%20umum%20pengadaan%20Tahun%202025_compressed_54166b6e21f1218d2c14a70db962ecc3.pdf).

3. **RUP participates in execution workflows, but an immutable one-to-one public join is unproven.** INAPROC documents selecting a RUP by code during catalogue checkout. The official SPSE 4.4 PPK guide also permits updating the RUP used by an already-running non-tender package. Record linkage evidence and observation time; do not use title similarity as a verified execution link or silently overwrite historical links. [INAPROC checkout guide](https://bantuan.inaproc.id/hc/id-id/articles/8167455220367-Memulai-Pesanan), [SPSE 4.4 PPK guide, section 5.3.3](https://bantuan.inaproc.id/hc/id-id/article_attachments/14247871985935).

4. **Execution-system data cannot be treated as uniformly anonymous public data.** LKPP has a separate auditor-account service; its contract-management instructions require SPSE accounts. INAPROC's non-tender instructions describe provider-specific invitations and qualified-provider access. These sources establish role-dependent workflows, not the completeness of anonymous tender tabs. The PRD's public participants, bids, evaluations, reasons, addresses and masked-NPWP claims remain source-by-source hypotheses. [LKPP auditor-account service](https://lkpp.go.id/layanan/mendapatkan-akun-auditor-di-aplikasi-spse), [contract management](https://www.lkpp.go.id/layanan/mengelola-kontrak), [non-tender provider workflow](https://bantuan.inaproc.id/hc/id-id/articles/17966076202383-Pengiriman-Data-Kualifikasi-dan-Penawaran).

5. **The universal Rp200 million split-package rule is incorrect.** In the official Perpres 46/2025 consolidation, Article 38(3) permits direct procurement up to Rp200 million for goods/other services and Rp400 million for construction; Article 41(3) uses Rp100 million for consultancy. Article 20(2)(d) prohibits intentional splitting to avoid tender/selection. Near-threshold values alone cannot establish that intent. Resolve procurement category, applicable regulation date, method and exceptions before emitting a review signal. This is engineering rule interpretation for review, not a legal conclusion about any package. [Official consolidated regulation, Articles 20, 38 and 41](https://jdih.lkpp.go.id/admin/uploads/documents/Konsolidasi%20Nomor%2046%20Tahun%202025_2780_1.pdf), [BPK status record: effective 30 April 2025, listed as applicable](https://peraturan.bpk.go.id/Details/318647/perpres-no-46-tahun-2025).

6. **A relevant regional price source exists; matchability and cap applicability still need validation.** Sukoharjo JDIH lists Perbup 2/2026 for 2026 and publishes its price-standard PDF, including units, prices and notes. Its catalogue also contains later-year standards and prior amendments. Capture fiscal year, jurisdiction, annex/page, unit, specification, tax treatment and legal applicability; reject draft PDFs and mismatched-year benchmarks. Do not rename every listed price a statutory maximum without checking the operative provision and exceptions. [Sukoharjo JDIH catalogue](https://jdih.sukoharjokab.go.id/jdih-v3/produk-hukum?search=STANDAR+-+HARGA+-+SATUAN), [Perbup 2/2026 PDF](https://jdih.sukoharjokab.go.id/file/dokumen/peraturan-bupati-sukoharjo-nomor-2-tahun-2026-tentang-standar-harga-satuan-tahun-anggaran-2026-2026-ooqqd.pdf).

## What was actually checked

Official register, service/help pages and regulation text were read through web research. No credentials, bulk scraping or authenticated data access were used.

| Target attempted through web reader | Result | Meaning |
| --- | --- | --- |
| `https://data.inaproc.id` and `/docs`, `/portal` | Tool returned Internal Error | Reachability and API/auth schema unresolved; not proof the service is down |
| `https://sirup.inaproc.id/sirup/home` | Tool returned Internal Error | No live source response captured |
| Candidate SIRUP detail route for PRD ID `65174830` | Tool returned Internal Error | ID, title, budget and endpoint shape remain unverified |
| `https://spse.inaproc.id/lkpp` | Tool returned Internal Error | No anonymous tender-field sample captured |

The detail route above was a candidate, not an officially documented contract. The other named PRD example IDs (`64154392`, `65028950`), allegations, national annual row count and 5,000-row target were not independently confirmed. Do not label those examples validated anomalies.

## Recommended gates before implementation

These are planning recommendations, not facts about source coverage.

1. **Source contract gate:** select one jurisdiction and fiscal year; obtain a permitted export or small anonymous sample. Save URL, retrieval date, checksum, access basis, original field names and missing-field counts. Document API authorization, redistribution terms, pagination and limits before scheduling ingestion. A public dashboard does not prove an unrestricted bulk API.
2. **Planning schema gate:** validate ID, owner/satker, amount, method, category and year. Preserve raw descriptions and quantities. Missing descriptions disable title/spec comparison; `1 Paket`, ambiguous quantities and mixed bundles disable item-unit comparisons. Missing data means insufficient evidence, not NORMAL.
3. **Execution gate:** capture a real planning-to-execution identifier relation plus accessible participant/bid/evaluation records for each demonstrated case. Model zero, one or several execution references and explicit verified/candidate/unavailable link states. Scope tender IDs by source portal until global uniqueness is proven. No evaluation data means no high-bid-disqualification claim; registered participants are not automatically submitted bidders.
4. **Identity gate:** masked NPWP, shared text addresses and fuzzy names create candidate associations, never confirmed shared ownership. Keep source-native vendor identities separate until review. AHU enrichment stays optional and requires provenance, authorization and privacy review.
5. **Benchmark gate:** manually validate a small set of comparable, correctly scoped SSH rows and regulation-backed threshold cases. Market listings are contextual observations, not legal ceilings or paid contract prices. Retain source page, timestamp and comparison assumptions.
6. **Fallback:** a curated, provenance-backed snapshot supports the core planning radar if API access remains unresolved. Show unavailable execution coverage explicitly. Synthetic graph fixtures may demonstrate software behavior only when prominently labelled; they cannot be presented as a real vendor ring.

Skipped: production adapters, authenticated portal/API tests, bulk downloads and live legal-case validation. Main risk: the PRD promises more source coverage and evidentiary certainty than this research establishes.
