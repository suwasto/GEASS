import json

from fastapi.testclient import TestClient
import pytest
from pydantic import ValidationError

from backend import app as service
from backend.execution import ObservedExecution, load_execution
from backend.observations import PlanningObservation
from backend.sources.lpse import parse_announcement
from backend.tests.test_lpse import ANNOUNCEMENT, TIMESTAMP, URL
from backend.tests.test_observations import record


def specimen():
    return parse_announcement(ANNOUNCEMENT, URL, TIMESTAMP)


def test_execution_snapshot_has_no_unobserved_bid_or_winner(tmp_path):
    source = specimen()
    path = tmp_path / "execution.json"
    path.write_text(json.dumps(source), encoding="utf-8")
    result = load_execution(path)
    assert result.kind == "non_tender" and result.id_rup == "456"
    assert result.signals == [] and result.nama_pemenang is None
    for mutation in ({"signals": ["Invented finding"]}, {"nama_pemenang": "Invented winner"},
                     {"kode_lelang": "999"}, {"rup_ids": ["456", "789"]}):
        with pytest.raises(ValidationError):
            ObservedExecution.model_validate({**source, **mutation})


def test_real_link_requires_exact_identifier_and_retains_missing_execution_fields(monkeypatch):
    execution = ObservedExecution.model_validate(specimen())
    monkeypatch.setattr(service, "OBSERVED_EXECUTION", execution)
    observation = record(id_rup="456", satker=execution.satker)
    monkeypatch.setattr(service, "OBSERVATIONS", [PlanningObservation.model_validate(observation)])
    client = TestClient(service.app, client=("127.0.0.1", 50000))
    row = client.get("/api/packages/456?dataset=observed").json()
    assert row["linkage"]["status"] == "verified_source_identifier"
    assert row["linkage"]["kind"] == "non_tender" and row["classification"] is None
    tender = client.get("/api/tenders/123?dataset=observed").json()
    assert tender["hps"] == "9007199254740992.99"
    assert tender["nama_pemenang"] is None
    graph = client.get("/api/tenders/123/graph?dataset=observed").json()
    assert len(graph["edges"]) == 1 and not graph["synthetic"]
    assert service.observation_view(PlanningObservation.model_validate(record(id_rup="999")))["linkage"]["status"] == "unavailable"
    remote = TestClient(service.app, client=("203.0.113.1", 50000))
    assert remote.get("/api/tenders/123?dataset=observed").status_code == 403
    assert remote.get("/api/tenders/123/graph?dataset=observed").status_code == 403
