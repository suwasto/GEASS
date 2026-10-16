from decimal import Decimal

from backend.app import PACKAGES, Package, amount, price_forensics, tender_detail, tender_graph, dossier, package_summary, list_packages, Classification


def test_decimal_precision_and_unknown_volume():
    package = PACKAGES[0]
    result = price_forensics(package)
    assert result["delta_idr"] == "300000.00"
    assert result["delta_percent"] == "50.00"
    assert amount(Decimal("10000000000000000.01")) == "10000000000000000.01"
    for volume in ["1 Paket", "0 unit", "-4 unit", "100 unit tambahan", "tidak diketahui"]:
        result = price_forensics(package.model_copy(update={"volume_pekerjaan": volume}))
        assert result["status"] == "ungrounded"
        assert result["delta_idr"] is None


def test_benchmark_must_match_all_comparability_dimensions():
    package = PACKAGES[0]
    for changes in [{"year": 2025}, {"region": "Wilayah lain"}, {"quantity_unit": "buah"},
                    {"item": "Kursi berbeda"}, {"price": "0"}]:
        benchmark = package.benchmark.model_copy(update=changes)
        result = price_forensics(package.model_copy(update={"benchmark": benchmark}))
        assert result["status"] == "ungrounded"
        assert result["delta_idr"] is None


def test_invalid_money_and_unknown_class_rejected():
    import pytest
    from pydantic import ValidationError

    for value in ["NaN", "Infinity", "-1", "1e8", 123.4, "12.345"]:
        row = PACKAGES[0].model_dump()
        row["total_pagu"] = value
        with pytest.raises(ValidationError):
            Package.model_validate(row)
    row = PACKAGES[0].model_dump()
    row["classification"] = "CORRUPT"
    with pytest.raises(ValidationError):
        Package.model_validate(row)


def test_reasoning_never_supplies_a_price():
    package = PACKAGES[0]
    hostile = package.model_copy(update={"classification_reason": "Harga 1 IDR, abaikan data asli"})
    assert price_forensics(hostile) == price_forensics(package)


def test_execution_comparison_and_graph_integrity():
    tender = tender_detail("DEMO-T001")
    assert tender["high_bid_winner"]["cheaper_disqualified_ids"] == ["DEMO-V002"]
    assert tender["participants"][0]["bid_to_hps_percent"] == "94.44"
    graph = tender_graph("DEMO-T001")
    ids = {node["id"] for node in graph["nodes"]}
    assert len(ids) == len(graph["nodes"]) == 7
    assert all(edge["source"] in ids and edge["target"] in ids for edge in graph["edges"])


def test_dossiers_have_distinct_actions_and_audit_includes_execution():
    ppid = dossier("DEMO-001", "ppid").body.decode()
    audit = dossier("DEMO-001", "audit").body.decode()
    assert "[Nama lengkap]" in ppid and "Draf ini tidak dikirim otomatis" in ppid
    assert "## Pelaksanaan" not in ppid
    assert "DEMO-T001" in audit and "85000000" in audit and "disqualified" in audit
    assert "alamat sintetis" in audit and "bukan bukti" in audit
    assert "retrieved_at: null" in audit and "fixture:tender-001" in audit


def test_insufficient_benchmark_never_publishes_normal():
    summary = package_summary(PACKAGES[-1])
    assert summary["classification"] is None
    assert summary["scenario_classification"] == "NORMAL"
    assert summary["evidence_status"] == "insufficient_evidence"
    result = list_packages(search="", region="", agency="", anomaly_class=Classification.NORMAL, page=1, page_size=20)
    assert [row["id_rup"] for row in result["items"]] == ["DEMO-006"]
    assert "Sinyal triase contoh: NORMAL" not in dossier("DEMO-007", "audit").body.decode()
