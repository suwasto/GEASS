# Does id_rup join to kode_lelang?

Labels: wayfinder:research
Type: research
Status: open
Blocked by: —

Related: 02 surfaced this as its unresolved risk; 07 depends on the answer because it decides whether the syndicate graph can be tied to a flagged planning package on screen.

## Question

Is there a real, published join between a SIRUP planning record (`id_rup`) and the LPSE tender that executed it (`kode_lelang`)?

This single field decides whether GEASS's second headline innovation is a system or a claim. The PRD asserts that GEASS "links the flagged `id_rup` planning package directly to its downstream execution on LPSE/SPSE." *LPSE / SPSE retrieval feasibility* found that PyProc exposes announcement, participants, evaluations, winner, and schedule — and never mentions `id_rup`.

Resolve:

- Does the SPSE package-detail payload carry `id_rup`, or any field that resolves to a RUP planning record?
- Is there a documented crosswalk between the two systems — a shared package identifier, an announcement field, or an LKPP mapping table? The ISB Satu Data master datasets are worth checking for one.
- If no direct join exists, is there a **reliable heuristic** — agency plus budget year plus package title plus `nilai_pagu_paket` matching `total_pagu`? How reliable is that in practice, and what is its false-match rate on a handful of real cases?
- **Does the SIRUP RUP record link outward instead?** Some planning records carry a downstream reference once a package goes to tender. Check the live `sirup.inaproc.id` detail page for any tender or `kode_lelang` reference — this is the cheaper direction and may have been overlooked.
- State plainly whether a bridged demo (a planner-side anomaly and a tender-side graph shown alongside each other, rather than provably joined) is the honest fallback.

## Answer

A yes with the field name and the join recipe, a yes-with-caveats including the heuristic and its reliability, or a no — in which case the video stops claiming lifecycle tracking and the map says so.

<!-- appended on resolution -->
