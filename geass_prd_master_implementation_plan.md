# GEASS: Government Expenditure Anomaly & Syndicate Surveillance

**Document Type:** Product Requirements Document (PRD), Public Data Schema Specification & Engineering Implementation Plan  
**Target Competition:** Google Cloud AI Builder Cup 2026 (JAPAC)  
**Target Track:** Sustainability & Social Impact (or BFSI: Intelligent Risk & Fraud)  
**Architecture Paradigm:** End-to-End Multi-Agent Procurement Surveillance & Collusion Graph System built natively on Google Cloud.

---

## 1. Executive Summary & Product Vision

Indonesia’s public procurement ecosystem generates over 3 million procurement planning rows annually across ministries, provinces, and regional governments (Pemda/Pemkot) via **SIRUP (Sistem Informasi Rencana Umum Pengadaan)** and executes trillions of IDR in tenders through **LPSE / SPSE (Sistem Pengadaan Secara Elektronik)**. 

Because human oversight cannot manually inspect millions of rows, two systemic failures occur every budget cycle:
1. **Budget Planning Absurdity & Disguised Markups (Pre-Tender):** Regional agencies bury non-essential, ceremonial, or wildly overpriced expenditures inside generic account codes—such as allocating IDR 200,000,000 for ceremonial flower arrangements (*karangan bunga/bunga tabur*), IDR 198,150,000 for a village recreational viewing tower (*Sky View*) unrelated to basic public services, or billions of IDR for VIP open-house catering.
2. **Tender Execution Collusion & Vendor Syndicates (Tender Phase):** When high-value packages proceed to tender or e-Purchasing, affiliated vendor rings (*sindikat tender*) manipulate competition—submitting cover bids, disqualifying lower-priced competitors on minor administrative technicalities, and rotating wins among companies sharing the same beneficial owners, addresses, or legal infrastructure.

### The GEASS Solution
**GEASS** (*Government Expenditure Anomaly & Syndicate Surveillance*) is an autonomous, multi-agent surveillance platform built on **Google Cloud ADK (Agent Development Kit)**, **Vertex AI (Gemini 2.5 Pro & Flash)**, and **BigQuery Graph**. 

**GEASS** delivers three core technical innovations for the Google Cloud AI Builder Cup:
1. **Neuro-Symbolic Price & Mandate Grounding:** Instead of relying purely on LLM intuition, GEASS pairs semantic reasoning with deterministic unit-price extraction, grounding SIRUP budgets against statutory regional price ceilings (**Pergub/Perbup SSH & SBU**) and live e-commerce/e-Katalog market benchmarks via **Vertex AI Search Grounding**.
2. **Planning-to-Tender Lifecycle Tracking (SIRUP $\rightarrow$ LPSE):** GEASS links the flagged `id_rup` planning package directly to its downstream execution on **LPSE/SPSE**, exposing who bid, who was disqualified (`alasan_gugur`), and who took home the contract.
3. **Autonomous Syndicate Graph & One-Tap Civic Action:** GEASS constructs an entity-relationship network in **BigQuery** to catch vendor cartels and generates one-tap, legally structured **PPID (Freedom of Information) / BPK / APIP Investigation Dossiers**.

---

## 2. Product Requirements Document (PRD)

### 2.1 Target Users ("Unlikely Heroes")
* **Investigative Data Journalists & Civic Watchdogs (ICW, Regional NGOs):** Need instant filtering of millions of SIRUP/LPSE rows into verifiable leads with ready-to-send PPID legal requests.
* **Internal Government Inspectors (APIP / Inspektorat Daerah & BPK Auditors):** Need pre-screened risk prioritization before annual regional budget evaluations.
* **Everyday Citizens:** Need a transparent, zero-login public dashboard that translates complex procurement codes into clear visual explanations of how local tax funds are spent.

### 2.2 Core Functional Modules

#### Module 1: The Absurdity & Markup Radar (SIRUP Pre-Tender Screening)
Structured around high-density tabular transparency (`ID`, `NAMA PAKET`, `PEMILIK`, `SATKER / LOKASI`, `PAGU`, `KLASIFIKASI`, `ALASAN`), enhanced with multi-vector evidence:
* **Capability 1 — Title vs. Specification Discrepancy Detection:** Evaluates whether `nama_paket` uses vague administrative wrapper naming (e.g., *"Belanja Alat/Bahan untuk Kegiatan Kantor Lainnya"*) to conceal ceremonial or consumptive items revealed only inside `uraian_pekerjaan` or `spesifikasi_pekerjaan` (e.g., *"Pengadaan karangan bunga/bunga tabur"* or *"dekorasi resepsi"*).
* **Capability 2 — Institutional Mandate Relevance (`Relevansi Lembaga`):** Evaluates whether the procuring agency (`satker`) and administrative tier (e.g., *Kelurahan*, *Sekretariat DPRD*, *Bagian Umum*) have a legitimate public-service mandate for the expenditure, flagging non-essential aesthetic/recreational builds (e.g., a *Kelurahan* building an IDR 198.15M *Sky View* tower) vs. core public infrastructure.
* **Capability 3 — Implied Unit Price & Statutory Cap Grounding:** Parses volume quantities from `volume_pekerjaan` and calculates the **Implied Unit Price**:
  $$\text{Implied Unit Price} = \frac{\text{Pagu Anggaran }(\texttt{total\_pagu})}{\text{Extracted Numeric Volume }(\texttt{volume\_pekerjaan})}$$
  Compares this unit cost against regional **SSH/SBU** (Standar Satuan Harga / Standar Biaya Umum) PDFs and live **Vertex AI Search** retail prices.
* **Multi-Class Classification Taxonomy:**
  * `ABSURD` (Ceremonial, non-essential, or severely disproportionate to public benefit)
  * `INDICATED MARKUP` (Unit price significantly exceeds SSH/SBU or retail market benchmark)
  * `SPECIFICATION LOCK / TAILORED` (Brand-pointing or overly restrictive specs designed to favor one vendor)
  * `SPLIT PACKAGE (PECAH PAKET)` (Multiple identical packages kept just under IDR 200,000,000 to avoid public tender and force *Pengadaan Langsung*)
  * `NORMAL` (Aligned with agency mandate and market pricing)

#### Module 2: The Syndicate & Cartel Graph (LPSE Execution Forensics)
Traces flagged `id_rup` packages into public LPSE tender announcements (`Pengumuman Lelang`, `Peserta`, `Hasil Evaluasi`, `Pemenang Berkontrak`):
* **Red-Flag Behavioral Detection:**
  * **High-Bid Winner Anomaly:** All lower-bidding vendors are disqualified during technical/administrative evaluation (`alasan_gugur`), leaving the highest bidder (clustered at $98\%–99.8\%$ of `nilai_hps`) as the sole winner.
  * **Cover Bidding (*Pendamping Tender*):** The exact same group of 3–5 vendors repeatedly enters tenders together across an agency, with the losing vendors never submitting a complete technical file.
  * **Physical & Identity Clustering:** Matches winning and losing vendors via masked NPWP prefixes, fuzzy company name normalization, and geocoded `alamat_pemenang` via **Google Maps Places API** (catching two "competing" companies registered at the exact same shophouse/ruko).
* **Interactive Network Graph UI:** Visualizes connections between `Satker`, `Paket Tender`, `Winning Vendor`, `Losing Cover Bidders`, `Shared Address/NPWP Prefix`, and `Enriched Corporate Officers (AHU)`.

#### Module 3: Adversarial Verification & Fortified Security Layer
* **Prosecutor vs. Defense Agent Debate:** Before publishing an `ABSURD` or `COLLUSION` badge, a **Prosecutor Agent** formulates the anomaly thesis while a **Defense Agent** searches for valid exceptions (e.g., remote geographic logistics, multi-year scope, or emergency maintenance). Only findings that survive this adversarial review are surfaced.
* **Google Cloud Model Armor Integration:** Protects the ingestion pipeline from adversarial prompt injection embedded inside public `spesifikasi_pekerjaan` fields or uploaded KAK/corporate PDFs (e.g., hidden instructions attempting to force the AI to classify a package as `NORMAL`).

#### Module 4: One-Tap Civic & Audit Action Dispatcher
* **Human-in-the-Loop Governance:** GEASS never accuses individuals of crimes autonomously; it outputs structured **Risk Signals & Evidence Dossiers**.
* **One-Tap Export Outputs:**
  1. **Draft Surat Permohonan Informasi Publik (PPID):** Legally formatted request under *UU No. 14 Tahun 2008 tentang Keterbukaan Informasi Publik* requesting the granular RKA/RAB and BAST for a flagged `id_rup`.
  2. **APIP / BPK Executive Risk Brief:** PDF/Markdown dossier detailing the exact `id_rup`, `kode_lelang`, markup delta in IDR, and vendor graph anomalies.

---

## 3. Comprehensive Data Parameter Specification & Feasibility Matrix

To guarantee 100% technical feasibility during the hackathon and withstand scrutiny from judges familiar with Indonesian civic data, GEASS strictly utilizes **existing, publicly accessible data schemas** supplemented by an optional crowd/auditor enrichment dropzone.

### 3.1 Dataset 1: SIRUP LKPP (`sirup.lkpp.go.id` / INAPROC Open Data)
* **Availability:** 100% Public (accessible via SIRUP public JSON endpoints and HTML package detail pages).
* **Granularity:** Package-level procurement plans (Penyedia & Swakelola).

| Parameter Name | Data Type | Example Value (Grounded in Real Data) | Role in GEASS |
| :--- | :--- | :--- | :--- |
| `id_rup` | `STRING` / `INT64` | `65174830`, `64154392`, `65028950` | Primary key linking budget planning to LPSE execution. |
| `nama_paket` | `STRING` | `"Belanja Alat/Bahan untuk Kegiatan Kantor-Alat/Bahan untuk Kegiatan Kantor Lainnya"` | Evaluated by **Capability 1** for vague wrapper naming vs. actual item bought. |
| `klpd` / `pemilik` | `STRING` | `"Kab. Sukoharjo (Pemkot/Pemkab)"` | Regional government or ministry owner. |
| `satker` | `STRING` | `"Bagian Umum"`, `"Kelurahan Gayam"`, `"Sekretariat DPRD"` | Evaluated by **Capability 2** for institutional mandate alignment. |
| `lokasi_pekerjaan` | `STRING` | `"Jawa Tengah, Sukoharjo (Kab.)"` | Used for regional SSH/SBU price index matching and geographic filtering. |
| `total_pagu` | `NUMERIC` | `200000000`, `198150000`, `188000000` | Total ceiling budget in IDR; numerator for Implied Unit Price and Pecah Paket checks. |
| `uraian_pekerjaan` | `STRING` | `"Pengadaan karangan bunga/bunga tabur..."` / `"Pengadaan dekorasi resepsi..."` | Reveals the true expenditure hidden behind generic `nama_paket` titles. |
| `spesifikasi_pekerjaan` | `STRING` | Technical specs, dimensions, or material requirements | Parsed for unit counts, quality tiers, and brand-pointing (`Specification Lock`). |
| `volume_pekerjaan` | `STRING` | `"1 Paket"`, `"500 Kotak"`, `"12 Bulan"` | Parsed into numeric quantities to compute Implied Unit Price. |
| `metode_pemilihan` | `STRING` | `"Pengadaan Langsung"`, `"E-Purchasing"`, `"Tender"` | Flags `Pecah Paket` when multiple identical packages sit just below IDR 200M using *Pengadaan Langsung*. |
| `jenis_pengadaan` | `STRING` | `"Barang"`, `"Pekerjaan Konstruksi"`, `"Jasa Lainnya"` | Routes package to appropriate price benchmark category. |
| `tahun_anggaran` | `INT64` | `2026`, `2027` | Tracks year-over-year budget inflation for identical packages. |

### 3.2 Dataset 2: LPSE / SPSE Public Tender Portals (`lpse.*.go.id`)
* **Availability:** 100% Public (Summary, Participants, Evaluation Results, and Winner tabs on every SPSE portal).
* **Feasibility Note:** Individual vendor bid attachments (`Dokumen Penawaran`) are encrypted by LKPP APENDO and are **not** publicly downloadable. GEASS relies strictly on the **100% public tabular evaluation records** exposed on SPSE HTML/API pages.

| Parameter Name | Data Type | Example Value | Role in GEASS |
| :--- | :--- | :--- | :--- |
| `kode_lelang` | `STRING` | `"10029384"` | Unique tender ID linked back to `id_rup`. |
| `nilai_pagu_paket` | `NUMERIC` | `1500000000` | Ceiling budget transferred from SIRUP (in IDR). |
| `nilai_hps` | `NUMERIC` | `1495000000` | Owner's Estimate (*Harga Perkiraan Sendiri*) in IDR. |
| `peserta_tender` | `ARRAY<STRUCT>` | List of registered participant companies | Builds co-bidding frequency matrices for cartel detection. |
| `npwp_peserta` | `STRING` | `"01.234.567.8-***.***"` | Partially masked NPWP; first 9 digits + KPP tax code used for entity resolution. |
| `harga_penawaran` | `NUMERIC` | `1489000000` | Submitted bid price per vendor in IDR; calculates bid-to-HPS ratio ($\frac{\text{Bid}}{\text{HPS}}$). |
| `hasil_evaluasi` | `STRUCT` | `lulus_admin`, `lulus_teknis`, `lulus_harga` | Identifies cases where cheaper bidders are systematically eliminated. |
| `alasan_gugur` | `STRING` | `"Jadwal pelaksanaan tidak sesuai KAK..."` | Analyzed by Gemini to detect overly pedantic or repetitive disqualification excuses. |
| `nama_pemenang` | `STRING` | `"CV Maju Jaya Mandiri"` | Winning vendor node in the BigQuery Syndicate Graph. |
| `alamat_pemenang` | `STRING` | `"Jl. Veteran No. 12, Sukoharjo"` | Geocoded via Google Maps Places API to detect shared physical offices across "rival" bidders. |

### 3.3 Dataset 3: Regional Statutory Price Caps & Corporate Enrichment
* **Tier 1 (Public JDIH Portals — `jdih.*.go.id`):** Regional **Pergub / Perbup / Perwali SSH & SBU** PDF documents containing official maximum unit prices in IDR (`kode_barang`, `uraian_barang`, `spesifikasi`, `satuan`, `harga_satuan_maksimum`).
* **Tier 2 (Auditor / Citizen Enrichment Dropzone):** Official **AHU (Administrasi Hukum Umum)** company profile PDFs or leaked KAK/RAB documents uploaded by journalists/auditors to unlock `nama_direktur`, `nama_komisaris`, `nama_notaris`, and `nomor_akta` in the Syndicate Graph.

---

## 4. Google Cloud Architecture (Optimized to Win AI Builder Cup)

Google Cloud AI Builder Cup judges score heavily on **Technical Merit & Gen AI Implementation (40%)** and **Innovation (25%)**, with a dedicated **$2,000 Best Use of Google Cloud AI Tools** prize. GEASS uses a production-grade, cloud-native Google architecture:

```
+-----------------------------------------------------------------------------------+
|                        DATA SOURCES & INGESTION LAYER                             |
|  [SIRUP Public Data]   [LPSE Tender Tables]   [JDIH SSH PDFs]   [Citizen Upload]  |
+----------+----------------------+--------------------+------------------+---------+
           |                      |                    |                  |
           v                      v                    |                  v
+-----------------------------------------------------------------------------------+
|  GOOGLE CLOUD MODEL ARMOR (Prompt Injection & Malicious Document Sanitization)    |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|               CLOUD RUN: GOOGLE ADK MULTI-AGENT ORCHESTRATOR                      |
|                                                                                   |
|  +-----------------------------+       +---------------------------------------+  |
|  | 1. Ingestion & Doc AI Agent | ----> | 2. Semantic Absurdity & Mandate Agent |  |
|  | (Document AI + Gemini Flash)|       | (Gemini 2.5 Pro + Anomaly Taxonomy)   |  |
|  +-----------------------------+       +-------------------+-------------------+  |
|                                                            |                      |
|  +-----------------------------+       +-------------------v-------------------+  |
|  | 4. Syndicate Graph Agent    | <---- | 3. Price Grounding & SSH Agent        |  |
|  | (BigQuery Graph + Maps API) |       | (Vertex AI Search + Deterministic SQL)|  |
|  +--------------+--------------+       +---------------------------------------+  |
|                 |                                                                 |
|                 v                                                                 |
|  +-----------------------------------------------------------------------------+  |
|  | 5. Adversarial Critic Loop (Prosecutor vs. Defense Agent) -> Dossier Output |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------+-----------------------------------------+
                                          |
           +------------------------------+------------------------------+
           v                              v                              v
+---------------------+      +-------------------------+      +---------------------+
|   BIGQUERY +        |      | VERTEX AI SEARCH &      |      | CLOUD TRACE /       |
|   BIGQUERY GRAPH    |      | GROUNDING (SSH & Web)   |      | OPENTELEMETRY LOGS  |
+---------------------+      +-------------------------+      +---------------------+
```

### Why This Specific Google Stack Maximizes Your Judging Score:
1. **Google ADK (Agent Development Kit) on Cloud Run:** Orchestrates 5 specialized agents with strict state handoffs and asynchronous checkpointing rather than a monolithic prompt.
2. **Neuro-Symbolic Split ("The AI Never Does Raw Math"):** Gemini 2.5 Flash extracts structured quantities and semantic classifications (`Absurd`, `Ceremonial`, `Mandate Mismatch`), while **BigQuery SQL** executes deterministic Z-score price anomaly calculations, Pecah Paket clustering, and graph traversal (`BigQuery Graph`).
3. **Vertex AI Search & Grounding:** Grounds every price markup claim against indexed **Pergub SSH/SBU PDFs** and live Indonesian e-commerce/e-Katalog listings in IDR.
4. **Google Cloud Model Armor:** Demonstrates enterprise security by neutralizing hidden prompt injections inside procurement descriptions before they reach Gemini.
5. **Cloud Trace & OpenTelemetry:** Provides live, inspectable reasoning traces in the Google Cloud Console (a mandatory proof-of-cloud requirement in Google hackathons).

---

## 5. Step-by-Step Implementation Plan

### Phase 1: Data Pipeline & BigQuery Foundation (Day 1)
1. **Curate the Benchmark Dataset (Real + High-Signal Cases):**
   * Load 5,000+ real public **SIRUP** rows into BigQuery (`geass_db.sirup_packages`), ensuring inclusion of real benchmark anomalies (such as the Kab. Sukoharjo ceremonial flower package `65174830` at IDR 200M, the Kelurahan Gayam Sky View package `64154392` at IDR 198.15M, Sekretariat DPRD reception decorations `65028950` at IDR 188M, VIP open-house catering at IDR 3.2B, and split IT procurement packages).
   * Load linked **LPSE** tender evaluation records (`geass_db.lpse_tenders` and `geass_db.lpse_participants`) representing co-bidding rings, high-bid winners where cheaper vendors failed administrative checks, and shared vendor addresses.
2. **Index Statutory Benchmarks in Vertex AI Search:**
   * Upload regional **SSH / SBU (Standar Satuan Harga)** PDF excerpts into a Vertex AI Search datastore for instant RAG grounding.

### Phase 2: Google ADK Multi-Agent Backend & Model Armor (Day 2)
1. **Build the 5-Agent ADK Pipeline (`FastAPI` + `google-genai` / `google-adk` on Cloud Run):**
   * **Agent 1 (`SpecNormalizerAgent`):** Uses `gemini-2.5-flash` with Structured Outputs (`response_schema`) to dissect `nama_paket`, `uraian_pekerjaan`, and `volume_pekerjaan` into normalized item category, true underlying item, numeric quantity, and unit type.
   * **Agent 2 (`MandateAbsurdityAgent`):** Evaluates the normalized item against the procuring `satker` mandate (e.g., *Bagian Umum*, *Kelurahan*, *DPRD*) to generate the **Classification Badge** (`Absurd`, `Markup Risk`, `Pecah Paket`, `Spec Lock`) and the structured Indonesian/English reasoning (`Alasan Menurut Keyakinan AI`).
   * **Agent 3 (`PriceGroundingAgent`):** Queries the Vertex AI Search SSH datastore and live web search to compare the package's Implied Unit Price in IDR against statutory caps.
   * **Agent 4 (`SyndicateGraphAgent`):** Executes parameterized **BigQuery SQL / Graph queries** via MCP (Model Context Protocol) tools to fetch co-bidding edges, bid-to-HPS ratios, and Google Maps geocoded address overlaps for the linked LPSE tender.
   * **Agent 5 (`AdversarialCriticAgent`):** Runs a 2-turn Prosecutor vs. Defense check and compiles the final **PPID / BPK Audit Dossier**.
2. **Wire Model Armor & OpenTelemetry:**
   * Add a pre-ingestion middleware check using **Google Cloud Model Armor** (with a live demo toggle to simulate a poisoned procurement specification) and stream execution spans to **Google Cloud Trace**.

### Phase 3: Interactive Surveillance Frontend & Canvas Graph UI (Day 3)
Build a high-impact dark-mode UI combining a high-density anomaly radar table with an interactive forensic investigation drawer:
1. **View 1 — The National & Regional Absurdity Radar:**
   * High-density dark table displaying `ID RUP`, `NAMA PAKET`, `PEMILIK`, `SATKER / LOKASI`, `PAGU (IDR)`, `KLASIFIKASI AI` (with glowing `Absurd`, `Markup`, `Pecah Paket` badges), and `ALASAN & BENCHMARK HARGA`.
   * Instant filters by Region (`Kab. Sukoharjo`, `DKI Jakarta`, `Jawa Timur`, etc.), Agency Type (`Sekretariat DPRD`, `Bagian Umum`, `Kelurahan`), and Anomaly Type.
2. **View 2 — Deep-Dive Forensic Drawer & Syndicate Graph (Interactive Canvas):**
   * Clicking any row opens a forensic view:
     * **Price & SSH Forensics:** Breakdown of the **SIRUP Planning Anomaly** (Title vs. True Spec, SSH Cap vs. Implied Price in IDR, Prosecutorial vs. Defense reasoning).
     * **LPSE Syndicate Graph:** Interactive **Force-Directed Syndicate Graph** showing how that package was executed on LPSE—highlighting the Winning Vendor, disqualified cheaper bidders (`alasan_gugur`), shared address/NPWP links, and an **"Enrich with AHU Deed"** dropzone.
3. **View 3 — One-Tap Action & Cloud Telemetry Bar:**
   * One-tap buttons to generate the **PPID Information Request Letter** or **BPK/APIP Investigation Brief**, alongside a live **"View Google Cloud ADK & Model Armor Trace"** inspector panel for judges.

### Phase 4: Cloud Deployment & 3-Minute Winning Pitch Video (Day 4)
1. **Deploy to Google Cloud Run:** Deploy the unified service and record a clean screen capture of the **Google Cloud Console** showing active Cloud Run revisions, BigQuery queries, and OpenTelemetry traces.
2. **Record the 3-Minute Demo Video:**
   * **0:00–0:40:** Show the real problem—millions of SIRUP rows hiding IDR 200M flower budgets, IDR 198.15M village *Sky Views*, and VIP open-house snacks.
   * **0:40–1:45:** Show **GEASS** scanning SIRUP packages, flagging `Absurd` and `Markup` rows with SSH price grounding in IDR, and clicking a row to reveal the **LPSE Vendor Syndicate Graph** lighting up in red.
   * **1:45–2:25:** Trigger the **Model Armor Poisoning Defense** demo and show the **Google Cloud Console** ADK traces.
   * **2:25–3:00:** Click **"Generate Official PPID / BPK Dossier"** for one-tap real-world civic impact.