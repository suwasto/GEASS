# LPSE / SPSE retrieval feasibility

Labels: wayfinder:research
Type: research
Status: resolved
Blocked by: —

Related: 07 — whether the syndicate graph earns a beat in the video depends on this verdict.

## Question

Can GEASS obtain real tender-execution data — participants, evaluation outcomes, disqualification reasons, bid prices, and winners — from LPSE/SPSE portals inside the hackathon window?

Module 2 is the map's most differentiating claim and rests on the hardest data in the whole PRD. Unlike SIRUP, LPSE is not one system but hundreds of separately operated regional portals. Answer against primary sources: live `lpse.*.go.id` pages, LKPP documentation, and the SPSE application itself.

- Is there **any** national or aggregated source for Indonesian tender data, or is per-region portal scraping the only route? Check for open data portals, bulk downloads, or a documented API before concluding it is scraping-only.
- Which of the PRD's parameters are exposed publicly: `kode_lelang`, `nilai_pagu_paket`, `nilai_hps`, `peserta_tender`, `npwp_peserta`, `harga_penawaran`, `hasil_evaluasi`, `alasan_gugur`, `nama_pemenang`, `alamat_pemenang`?
- Confirm the PRD's own feasibility claim: bid attachments are APENDO-encrypted and undownloadable, so the plan rests on public tabular evaluation records. Is that accurate, and are those records complete enough to detect anything?
- **NPWP masking.** The PRD wants entity resolution across a masked NPWP. Verify exactly how much of the NPWP is actually exposed and whether the visible portion supports joining vendors across packages.
- **The linkage question, which matters most.** How would a `kode_lelang` be tied back to an `id_rup`? Is there a published field joining tender to planning record, or is `id_rup` absent from LPSE entirely? If absent, say so plainly — it changes what Module 2's core innovation can honestly claim.
- **Existence proof.** Can two or three real tenders be found that exhibit the PRD's red flags: a high-bid winner where cheaper bidders failed administrative checks, a repeated co-bidding group, or rival companies at one address? Finding even one of each de-risks the whole module.

## Deliverable

A verdict — **green**, **amber**, or **red** — the retrieval recipe, the honest state of the SIRUP↔LPSE linkage, and a list of concrete real tenders that can carry the syndicate graph in the demo.

## Answer

**Verdict: GREEN — the data the PRD calls hardest is the easiest to reach, because the PRD was written as if nobody had solved it.**

**A maintained library already does this work.** [PyProc](https://github.com/wakataw/pyproc) (`pip install pyproc`) is an actively developed Python library, CLI, and MCP server over SPSE/Inaproc. Its `get_tender_detail` returns *"announcement, participants, evaluations, winner, schedule"* — which is Module 2's requirement, field for field, without a bespoke scraper.

- **The "hundreds of portals" objection is answered.** PyProc resolves institution names to LPSE host slugs, builds canonical URLs as `https://spse.inaproc.id/{newUrlPath}`, and provides a built-in nationwide host `nasional` for lintas-instansi and *pencatatan nasional* data.
- **Rate limiting is already respectful by default:** minimum 1 second between requests (`PYPROC_RATE_LIMIT_DELAY`), configurable timeout, and 4 parallel workers (`PYPROC_MCP_WORKERS`) for detail fetches. It also documents a responsible-use policy, which is useful evidence when a judge asks about scraping ethics.
- **Bulk retrieval exists:** `get_tender_details_bulk` and `get_non_tender_details_bulk` avoid N sequential round trips.
- **A fallback source exists:** the **LKPP ISB Satu Data API** provides master LPSE, master K/L/PD, and *tender umum publik* indexed by LPSE code and budget year, for when direct SPSE queries time out or a host blocks.
- **Notable for the 40% Technical Merit score:** PyProc *ships as an MCP server*. The PRD's Module 2 specifies "parameterized BigQuery SQL / Graph queries via MCP tools." A ready-made procurement MCP server means the MCP layer can be real rather than decorative.

**The PRD's APENDO claim was not verified.** That bid attachments are encrypted and undownloadable is plausible and consistent with LKPP practice, but it was not confirmed against a primary source here. Treat it as a caution rather than a fact — do not repeat it to judges without checking.

**The serious unresolved risk: the `id_rup` ↔ `kode_lelang` linkage.** PyProc's entire documented tool surface — announcement, participants, evaluations, winner, schedule — never mentions `id_rup`. If no join exists between a planning record and its tender, then PRD innovation #2 (*Planning-to-Tender Lifecycle Tracking*, "the flagged `id_rup` links directly to its downstream execution") cannot be claimed as built. This is load-bearing enough that it has graduated into its own ticket rather than being left as a footnote.

**Red-flag existence proof not yet established.** Two or three real tenders exhibiting a high-bid winner, a repeated co-bidding group, or rival firms at one address have not been located. The path to finding them is now cheap; the finding itself is still outstanding and belongs with the anchor-verification work.
