# 19: SSH grounding and the implied unit price

**What to build:** Every price claim grounded in a real statute — the current regional SSH extracted into structured rows, with the implied unit price and its delta from the cap computed deterministically in IDR.

**Blocked by:** 17 (*Per-package detail crawl*)

**Status:** ready-for-agent

- [ ] The current Sukoharjo SSH regulation extracted into rows carrying `kode_barang`, `uraian_barang`, `spesifikasi`, `satuan` and `harga_satuan_maksimum`.
- [ ] Whether the document carries a text layer is established against the real file first; if it does not, the pre-extracted table path is used and the interface says so rather than grounding against nothing.
- [ ] The implied unit price is `total_pagu` divided by the parsed numeric volume, computed in deterministic code and never by a model.
- [ ] A grounded package shows its implied unit price, the statutory cap, and the delta between them in IDR.
- [ ] A package whose volume cannot be parsed into items is recorded as ungrounded and shows no computed delta, rather than a delta built on a guessed denominator.
- [ ] The regulation that supplied each benchmark is named beside the figure.
- [ ] A package with no applicable cap says so explicitly instead of appearing normal.
- [ ] The arithmetic, including the ungrounded case, is covered by tests over fixture values.
