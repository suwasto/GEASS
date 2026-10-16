from fastapi.testclient import TestClient

from backend import app as service
from backend.observations import PlanningObservation
from backend.tests.test_observations import record


def test_unavailable_public_data_never_silently_becomes_fixtures(monkeypatch):
    monkeypatch.setattr(service, "OBSERVATIONS", [])
    client = TestClient(service.app, client=("127.0.0.1", 50000))
    assert client.get("/api/packages?dataset=observed").status_code == 503
    assert client.get("/api/packages/00001234?dataset=observed").status_code == 404


def test_observed_public_facts_are_separate_from_synthetic_findings(monkeypatch):
    monkeypatch.setattr(service, "OBSERVATIONS", [PlanningObservation.model_validate(record())])
    client = TestClient(service.app, client=("127.0.0.1", 50000))
    assert client.get("/api/datasets").json()["default"] == "observed"
    listing = client.get("/api/packages?dataset=observed").json()
    assert listing["total"] == 1 and not listing["items"][0]["synthetic"]
    assert client.get("/api/packages?dataset=observed&anomaly_class=NORMAL").json()["total"] == 0
    detail = client.get("/api/packages/00001234?dataset=observed").json()
    assert detail["classification"] is None and not detail["dossier_available"]
    assert detail["linkage"]["status"] == "unavailable"
    assert client.get("/api/packages/00001234/dossier").status_code == 404
    assert all(row["synthetic"] for row in client.get("/api/packages").json()["items"])
    assert client.get("/api/health").json()["sources"]["sirup"]["status"] == "snapshot_loaded"


def test_real_capture_access_cannot_be_enabled_by_forging_forwarded_header(monkeypatch):
    monkeypatch.setattr(service, "OBSERVATIONS", [PlanningObservation.model_validate(record())])
    client = TestClient(service.app, client=("203.0.113.1", 50000), headers={"X-Forwarded-For": "127.0.0.1"})
    assert client.get("/api/datasets").json()["default"] == "fixture"
    assert client.get("/api/packages?dataset=observed").status_code == 403
    assert client.get("/api/packages/00001234?dataset=observed").status_code == 403
