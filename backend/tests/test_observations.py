import json

import pytest
from pydantic import ValidationError

from backend.observations import PlanningObservation, load_snapshot


def record(**changes):
    result = {"id_rup": "00001234", "nama_paket": "Synthetic parser test", "satker": "Test agency",
            "region": "Kabupaten Sukoharjo", "tahun_anggaran": 2026, "total_pagu": "9007199254740993",
            "source_url": "https://sirup.inaproc.id/sirup/home/detailPaketPenyediaPublic2017/00001234", "retrieved_at": "2026-10-16T12:00:00+07:00",
            "source_sha256": "a" * 64, **changes}
    if "id_rup" in changes and "source_url" not in changes:
        result["source_url"] = "https://sirup.inaproc.id/sirup/home/detailPaketPenyediaPublic2017/" + changes["id_rup"]
    return result


def test_source_facts_never_become_normal_or_fabricated_comparisons():
    row = PlanningObservation.model_validate(record()).public_view()
    assert row["total_pagu"] == "9007199254740993"
    assert row["id_rup"] == "00001234"
    assert row["classification"] is None
    assert row["price_forensics"]["delta_idr"] is None
    assert row["description"] is None and not row["coverage"]["description"]
    assert row["synthetic"] is False and row["dossier_available"] is False


@pytest.mark.parametrize("changes", [
    {"source_url": "javascript:alert(1)"}, {"source_url": "https://attacker.test/"},
    {"source_url": "https://secret@sirup.inaproc.id/"}, {"retrieved_at": "2026-10-16T12:00:00"},
    {"total_pagu": "NaN"}, {"total_pagu": "-1"}, {"source_sha256": "missing"},
    {"source_url": "https://sirup.inaproc.id/sirup/home/detailPaketPenyediaPublic2017/999"},
])
def test_invalid_source_boundary_is_rejected(changes):
    with pytest.raises((ValidationError, ValueError)):
        PlanningObservation.model_validate(record(**changes))


def test_snapshot_rejects_duplicates_and_wrong_scope(tmp_path):
    path = tmp_path / "observations.json"
    path.write_text(json.dumps({"records": [record()]}), encoding="utf-8")
    rows, digest = load_snapshot(path)
    assert len(rows) == 1 and len(digest) == 64
    for rows in ([record(), record()], [record(tahun_anggaran=2025)], [record(region="Another region")]):
        path.write_text(json.dumps({"records": rows}), encoding="utf-8")
        with pytest.raises(ValueError):
            load_snapshot(path)
