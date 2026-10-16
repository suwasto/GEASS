"""Offline, explicitly synthetic procurement review slice. No cloud adapters are implied."""
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
import json
import os
from pathlib import Path
import re
from time import perf_counter
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict, Field

ROOT = Path(__file__).resolve().parent
MONEY = r"^\d+(?:\.\d{1,2})?$"


class Classification(str, Enum):
    ABSURD = "ABSURD"
    MARKUP = "INDICATED MARKUP"
    LOCK = "SPECIFICATION LOCK"
    SPLIT = "SPLIT PACKAGE"
    NORMAL = "NORMAL"


class Benchmark(BaseModel):
    model_config = ConfigDict(extra="forbid")
    item: str
    quantity_unit: str
    price: str = Field(pattern=MONEY)
    region: str
    year: int
    document: str
    source_id: str


class Package(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id_rup: str
    nama_paket: str
    satker: str
    region: str
    total_pagu: str = Field(pattern=MONEY)
    tahun_anggaran: int
    description: str
    volume_pekerjaan: str
    normalized_item: str
    classification: Classification
    classification_reason: str
    benchmark: Benchmark | None
    tender_id: str | None


def now():
    return datetime.now(timezone.utc).isoformat()


def provenance(stage, computed=False, source_id="fixture:packages.json"):
    return {"stage": stage, "source_id": source_id, "retrieved_at": None,
            "computed": computed, "model_asserted": False, "synthetic": True,
            "note": "Data buatan untuk pengujian lokal; tidak diambil dari sumber pemerintah."}


def load_packages():
    rows = json.loads((ROOT / "fixtures" / "packages.json").read_text(encoding="utf-8"))
    packages = [Package.model_validate(row) for row in rows]
    if len({p.id_rup for p in packages}) != len(packages):
        raise ValueError("Duplicate fixture package identifier")
    return packages


def amount(value):
    return format(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), "f")


def price_forensics(package):
    result = {"status": "ungrounded", "reason": "Volume tidak terurai menjadi jumlah dan satuan barang.",
              "quantity": None, "unit": None, "implied_unit_price": None,
              "benchmark_unit_price": None, "delta_idr": None, "delta_percent": None,
              "source": None, "provenance": provenance("deterministic_decimal_price", True)}
    # Only explicit item counts qualify; a generic '1 Paket' is never a denominator.
    match = re.fullmatch(r"([0-9]+(?:[.,][0-9]+)?)\s+(unit|buah|pcs)", package.volume_pekerjaan.strip(), re.I)
    if not match:
        return result
    quantity = Decimal(match[1].replace(",", "."))
    if quantity <= 0:
        result["reason"] = "Jumlah harus lebih besar dari nol."
        return result
    unit = match[2].lower()
    implied = Decimal(package.total_pagu) / quantity
    result.update(quantity=str(quantity), unit=unit, implied_unit_price=amount(implied))
    benchmark = package.benchmark
    if benchmark is None:
        result["reason"] = "Tidak ada pembanding yang dapat diperiksa; selisih tidak dihitung."
        return result
    if (benchmark.item != package.normalized_item or benchmark.quantity_unit != unit
            or benchmark.region != package.region or benchmark.year != package.tahun_anggaran):
        result["reason"] = "Barang, satuan, wilayah, atau tahun pembanding tidak cocok."
        return result
    cap = Decimal(benchmark.price)
    if cap <= 0:
        result["reason"] = "Harga pembanding tidak valid."
        return result
    result.update(status="grounded", reason="Perbandingan deterministik dengan pembanding sintetis, bukan SSH nyata.",
                  benchmark_unit_price=amount(cap), delta_idr=amount(implied - cap),
                  delta_percent=amount((implied - cap) / cap * 100), source=benchmark.model_dump())
    return result


PACKAGES = load_packages()
ANONYMIZE = os.getenv("GEASS_ANONYMIZE", "").lower() in {"1", "true", "yes"}
RUNS = {}
app = FastAPI(title="GEASS — synthetic local prototype", version="0.1.0")
templates = Jinja2Templates(directory=str(ROOT / "templates"))
(ROOT / "static").mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(ROOT / "static")), name="static")


def find_package(id_rup):
    package = next((p for p in PACKAGES if p.id_rup == id_rup), None)
    if package is None:
        raise HTTPException(404, "Package not found")
    return package


def agency_name(name):
    return f"Instansi {sorted({p.satker for p in PACKAGES}).index(name) + 1:03d}" if ANONYMIZE else name


def vendor_name(index):
    return f"Penyedia {index:03d}" if ANONYMIZE else f"Vendor Sintetis {chr(64 + index)}"


def package_summary(package):
    data = package.model_dump(mode="json", exclude={"benchmark", "tender_id"})
    data["satker"] = agency_name(package.satker)
    price = price_forensics(package)
    insufficient = package.classification == Classification.NORMAL and price["status"] == "ungrounded"
    data["scenario_classification"] = data["classification"]
    if insufficient:
        data["classification"] = None
        data["classification_reason"] = "Belum dinilai: tidak tersedia pembanding yang cocok; ketiadaan sinyal bukan bukti kewajaran harga."
    return {**data, "evidence_status": "insufficient_evidence" if insufficient else "synthetic_fixture", "synthetic": True,
            "provenance": provenance("curated_synthetic_fixture"),
            "price_forensics": price}


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@app.get("/api/packages")
def list_packages(search: str = Query("", max_length=200), region: str = "", agency: str = "",
                  anomaly_class: Classification | None = None, page: int = Query(1, ge=1),
                  page_size: int = Query(20, ge=1, le=100)):
    rows = [p for p in PACKAGES if (not region or p.region == region)
            and (not agency or agency_name(p.satker) == agency)
            and (anomaly_class is None or package_summary(p)["classification"] == anomaly_class.value)
            and (not search or search.casefold() in " ".join([p.id_rup, p.nama_paket, p.description, p.normalized_item, p.satker]).casefold())]
    start = (page - 1) * page_size
    return {"items": [package_summary(p) for p in rows[start:start + page_size]], "total": len(rows),
            "page": page, "page_size": page_size, "regions": sorted({p.region for p in PACKAGES}),
            "agencies": sorted({agency_name(p.satker) for p in PACKAGES})}


@app.get("/api/packages/{id_rup}")
def package_detail(id_rup: str):
    package = find_package(id_rup)
    return {**package_summary(package), "supporting_evidence": [package_summary(package)["classification_reason"]],
            "counterevidence": ["Spesifikasi rinci, pajak, pengiriman, kebutuhan kegiatan, dan dokumen evaluasi nyata belum tersedia."],
            "linkage": {"status": "synthetic_join" if package.tender_id else "not_linked", "tender_id": package.tender_id,
                        "reason": "Relasi contoh eksplisit dalam fixture; bukan bukti join SIRUP–LPSE." if package.tender_id else "Tidak ada tender terkait yang diverifikasi."},
            "review_status": "synthetic_scenario_not_a_finding"}


@app.get("/api/tenders/{tender_id}")
def tender_detail(tender_id: str):
    if tender_id != "DEMO-T001":
        raise HTTPException(404, "Tender not found")
    hps = Decimal("90000000")
    participants = [
        {"id": "DEMO-V001", "nama_peserta": "Vendor Sintetis A", "bid": "85000000", "evaluation": "winner", "alasan_gugur": None},
        {"id": "DEMO-V002", "nama_peserta": "Vendor Sintetis B", "bid": "72000000", "evaluation": "disqualified", "alasan_gugur": "Skenario: dokumen teknis belum lengkap; belum diverifikasi."},
        {"id": "DEMO-V003", "nama_peserta": "Vendor Sintetis C", "bid": "80000000", "evaluation": "qualified", "alasan_gugur": None}]
    for participant in participants:
        participant["bid_to_hps_percent"] = amount(Decimal(participant["bid"]) / hps * 100)
        participant["nama_peserta"] = vendor_name(int(participant["id"][-3:]))
    winner = next(participant for participant in participants if participant["evaluation"] == "winner")
    cheaper_disqualified = [participant["id"] for participant in participants
                           if participant["evaluation"] == "disqualified" and Decimal(participant["bid"]) < Decimal(winner["bid"])]
    return {"id": tender_id, "kode_lelang": tender_id, "id_rup": "DEMO-001", "nama_tender": "Tender kursi sintetis",
            "hps": amount(hps), "nama_pemenang": vendor_name(1), "participants": participants,
            "signals": ["Contoh: pemenang memiliki penawaran di atas peserta yang gugur; dasar evaluasi perlu diperiksa."] if cheaper_disqualified else [],
            "high_bid_winner": {"detected": bool(cheaper_disqualified), "cheaper_disqualified_ids": cheaper_disqualified,
                                "explanation": "Perbandingan penawaran sintetis saja; kelengkapan dokumen dan kriteria evaluasi dapat menjelaskan hasil."},
            "schedule": [], "synthetic": True, "provenance": provenance("synthetic_execution_comparison", True, "fixture:tender-001")}


@app.get("/api/tenders/{tender_id}/graph")
def tender_graph(tender_id: str):
    tender = tender_detail(tender_id)
    nodes = [{"id": "agency", "label": agency_name("Dinas Contoh A"), "type": "agency"},
             {"id": "DEMO-001", "label": "Paket DEMO-001", "type": "package"},
             {"id": tender_id, "label": "Tender sintetis", "type": "tender"}]
    edges = [{"source": "agency", "target": "DEMO-001", "label": "merencanakan (contoh)"},
             {"source": "DEMO-001", "target": tender_id, "label": "relasi fixture"}]
    for participant in tender["participants"]:
        nodes.append({"id": participant["id"], "label": participant["nama_peserta"], "type": participant["evaluation"]})
        edges.append({"source": tender_id, "target": participant["id"], "label": participant["evaluation"]})
    nodes.append({"id": "DEMO-ADDR001", "label": "Alamat sintetis bersama", "type": "shared_address"})
    for vendor in ["DEMO-V001", "DEMO-V002"]:
        edges.append({"source": vendor, "target": "DEMO-ADDR001", "label": "alamat contoh cocok; perlu verifikasi"})
    return {"nodes": nodes, "edges": edges,
            "signals": tender["signals"] + ["Dua vendor contoh berbagi alamat sintetis; bukan bukti afiliasi atau kolusi."], "synthetic": True,
            "provenance": provenance("bounded_fixture_graph", True, "fixture:tender-001"),
            "limitations": ["Kesamaan alamat adalah skenario sintetis untuk ditinjau, bukan bukti hubungan nyata.",
                            "Tidak ada pengelompokan NPWP atau pengulangan peserta lintas tender yang diverifikasi."]}


@app.get("/api/packages/{id_rup}/dossier", response_class=PlainTextResponse)
def dossier(id_rup: str, kind: Literal["ppid", "audit"] = "ppid"):
    package = find_package(id_rup)
    price = price_forensics(package)
    summary = package_summary(package)
    classification = summary["classification"] or "Belum dinilai: bukti pembanding tidak cukup"
    title = "Draf Permohonan Informasi Publik (PPID)" if kind == "ppid" else "Draf Catatan Risiko APIP/BPK"
    if kind == "ppid":
        purpose = """## Identitas dan tujuan permohonan

Kepada: [Nama/jabatan PPID dan alamat instansi]
Pemohon: [Nama lengkap]
Alamat/kontak: [Lengkapi sesuai kebutuhan permohonan]
Tanggal: [Tanggal permohonan]
Tujuan penggunaan informasi: [Lengkapi tujuan yang sah]
Cara menerima informasi: [Salinan elektronik/alamat tujuan]

Mohon informasi dan salinan dokumen berikut untuk paket di bawah ini:

1. KAK dan spesifikasi teknis rinci beserta dasar kebutuhan.
2. Rincian volume, satuan, komponen biaya, pajak, dan logistik.
3. Dasar penetapan harga, dokumen pembanding, dan ruang lingkup penerapannya.
4. Dokumen evaluasi peserta, alasan gugur, serta penetapan hasil bila tersedia.
5. Penjelasan hubungan paket perencanaan dengan tender pelaksanaan bila ada.

Jika dokumen belum tersedia atau tidak dapat diberikan, mohon penjelasan dan petunjuk prosedur yang berlaku.

Hormat saya,
[Nama/tanda tangan pemohon]

**Wajib dilengkapi manusia:** identitas, penerima, tanggal, dan tujuan; periksa persyaratan instansi sebelum penggunaan. Draf ini tidak dikirim otomatis.
"""
    else:
        purpose = """## Tujuan catatan risiko

Bahan prioritas pemeriksaan APIP/BPK, bukan temuan audit atau penetapan pelanggaran. Pemeriksa perlu meminta dokumen primer dan menguji penjelasan alternatif sebelum menarik kesimpulan.

## Pelaksanaan dan hubungan peserta
"""
        if package.tender_id:
            tender = tender_detail(package.tender_id)
            graph = tender_graph(package.tender_id)
            purpose += f"\nTender contoh: {tender['id']}; pemenang contoh: {tender['nama_pemenang']}; HPS: IDR {tender['hps']}.\n"
            for participant in tender["participants"]:
                purpose += f"\n- {participant['nama_peserta']}: penawaran IDR {participant['bid']}; {participant['bid_to_hps_percent']}% HPS; evaluasi {participant['evaluation']}; alasan: {participant['alasan_gugur'] or 'tidak tercatat dalam fixture'}.\n"
            purpose += "\n" + "\n".join(tender["signals"] + graph["signals"][-1:] + graph["limitations"])
            purpose += "\nSumber pelaksanaan dan graf: fixture:tender-001; relasi hanya synthetic_join, bukan join pengadaan nyata. Waktu pengambilan: null (tidak ada sumber live).\n"
        else:
            purpose += "\nTidak ada tender terkait yang diverifikasi; tidak ada klaim lintas tahap atau hubungan vendor.\n"
        purpose += "\n## Penjelasan alternatif dan tindak lanjut\n\n" + "\n".join(package_detail(id_rup)["counterevidence"])
        purpose += "\nMinta rincian spesifikasi, komponen biaya, dasar evaluasi, dan verifikasi alamat; kesamaan alamat saja tidak membuktikan afiliasi.\n"
    text = f"""# {title}

**CONTOH SINTETIS — bukan kasus nyata; jangan dikirim sebagai permohonan atas paket nyata.**

{purpose}

## Paket dan sinyal triase

Paket: {package.id_rup} — {package.nama_paket}
Unit kerja: {agency_name(package.satker)}; wilayah: {package.region}; tahun: {package.tahun_anggaran}
Pagu contoh: IDR {package.total_pagu}
Uraian contoh: {package.description}

Sinyal triase contoh: {classification}. {summary['classification_reason']}

## Perhitungan deterministik

Volume sumber: {package.volume_pekerjaan}; jumlah terurai: {price['quantity'] or 'tidak tersedia'}; satuan: {price['unit'] or 'tidak tersedia'}.
Metode: pagu dibagi jumlah yang dapat diperiksa; selisih adalah harga satuan dikurangi pembanding; persentase adalah selisih dibagi pembanding dikali 100. Tidak ada tebakan untuk volume paket gabungan.
Harga satuan terhitung: {price['implied_unit_price'] or 'tidak dapat dihitung'} IDR.
Pembanding sintetis: {price['benchmark_unit_price'] or 'tidak tersedia'} IDR.
Selisih satuan: {price['delta_idr'] or 'tidak dapat dihitung'} IDR; {price['delta_percent'] or 'tidak dapat dihitung'}%.
Dasar perbandingan: {price['reason']}
Sumber pembanding: {price['source']['source_id'] + ' — ' + price['source']['document'] if price['source'] else 'tidak ada pembanding yang cocok'}.

Informasi ini merupakan permintaan klarifikasi, bukan pernyataan adanya pelanggaran. Perbedaan spesifikasi, pajak, logistik, dan kebutuhan operasional dapat menjelaskan perbedaan harga. Kesesuaian dasar hukum dan tujuan permohonan perlu diperiksa sebelum penggunaan nyata.

Provenans: fixture:packages.json, baris dengan id_rup {package.id_rup}; tahap curated_synthetic_fixture dan deterministic_decimal_price; klasifikasi dikurasi sebagai skenario, angka dihitung dengan Decimal, tanpa keluaran model. Data tidak diambil dari SIRUP/LPSE/JDIH dan tidak memiliki waktu pengambilan sumber (retrieved_at: null). Relasi tender hanya contoh bila tersedia.
"""
    return PlainTextResponse(text, media_type="text/markdown", headers={"Content-Disposition": f'attachment; filename="geass-{id_rup}-{kind}.md"'})


@app.get("/api/health")
def health():
    names = ["sirup", "lpse", "jdih", "bigquery", "gemini", "model_armor", "cloud_trace"]
    return {"status": "degraded", "mode": "synthetic_fixture", "local_ready": True,
            "sources": {name: {"status": "not_connected", "reason": "Integrasi live belum dikonfigurasi atau diuji."} for name in names},
            "limitations": ["Semua data adalah contoh buatan, bukan data pengadaan nyata.",
                            "Tidak ada inference AI, proteksi Model Armor, atau Cloud Trace aktif.",
                            "Run dan span lokal disimpan sementara dalam memori proses."]}


class RunRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    mode: Literal["fixture"]


@app.post("/api/runs", status_code=201)
def create_run(body: RunRequest):
    start = now()
    timer = perf_counter()
    # Validate the same checked-in corpus every run; fixture ingestion never fetches a URL.
    packages = load_packages()
    for package in packages:
        price_forensics(package)
    end = now()
    run_id = uuid4().hex
    run = {"id": run_id, "status": "completed", "mode": body.mode, "started_at": start,
           "finished_at": end, "package_count": len(packages), "model_calls": 0,
           "spans": [{"name": "validate_and_price_synthetic_fixture", "status": "completed", "started_at": start,
                      "finished_at": end, "duration_ms": round((perf_counter() - timer) * 1000, 3),
                      "source": "local_process", "package_count": len(packages)}],
           "provenance": provenance("local_fixture_validation", True)}
    # Bounded, ephemeral run history for the local demonstration.
    if len(RUNS) >= 100:
        RUNS.pop(next(iter(RUNS)))
    RUNS[run_id] = run
    return run


@app.get("/api/runs/{run_id}")
def get_run(run_id: str):
    if run_id not in RUNS:
        raise HTTPException(404, "Run not found (local history is ephemeral)")
    return RUNS[run_id]
