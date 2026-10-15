# 16: Real SIRUP rows on the radar

**What to build:** The radar table, populated with real SIRUP packages for a real region from LKPP's bulk open-data export, filterable and paged — the first surface a user actually reads.

**Blocked by:** 15 (*Deployed walking skeleton*)

**Status:** ready-for-agent

- [ ] Real package rows loaded from the bulk open-data export, carrying `id_rup`, `nama_paket`, `satker`, `klpd` or `pemilik`, `lokasi_pekerjaan`, `total_pagu`, `metode_pemilihan` and `tahun_anggaran` wherever the source supplies them.
- [ ] The loaded set is large enough that a judge sees scale behind the table rather than a toy sample.
- [ ] The listing filters by region, agency type and anomaly class, with stable paging and an accurate total count.
- [ ] Every row carries a provenance envelope naming its source, its retrieval timestamp, and that its figures are computed rather than model-asserted.
- [ ] The dark radar table renders legibly at 720p, with the column set chosen for that resolution, and figures displayed in IDR.
- [ ] A row whose source omits a field shows it as unknown, never as zero or blank.
- [ ] An empty filter result renders an honest empty state rather than an error or a blank table.
- [ ] The listing contract and its filters are covered by a test running against the recorded specimens with no network access.
