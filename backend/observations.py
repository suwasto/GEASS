"""Read operator-captured planning facts without turning them into findings."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class PlanningObservation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id_rup: str = Field(pattern=r"^\d{1,30}$")
    nama_paket: str = Field(min_length=1, max_length=2000)
    satker: str = Field(min_length=1, max_length=500)
    region: str = Field(min_length=1, max_length=500)
    tahun_anggaran: int = Field(ge=2000, le=2100)
    total_pagu: str | None = Field(default=None, pattern=r"^\d{1,29}(?:\.\d{1,2})?$")
    description: str | None = Field(default=None, max_length=20000)
    spesifikasi_pekerjaan: str | None = Field(default=None, max_length=20000)
    volume_pekerjaan: str | None = Field(default=None, max_length=2000)
    metode_pemilihan: str | None = Field(default=None, max_length=300)
    source_url: str
    retrieved_at: datetime
    source_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")

    @field_validator("source_url")
    @classmethod
    def public_sirup_url(cls, value):
        url = urlsplit(value)
        if (url.scheme != "https" or url.hostname != "sirup.inaproc.id"
                or url.username or url.password or url.port not in (None, 443)):
            raise ValueError("Expected an HTTPS public SIRUP locator")
        return value

    @field_validator("retrieved_at")
    @classmethod
    def require_timezone(cls, value):
        if value.utcoffset() is None:
            raise ValueError("Observation time needs an explicit UTC offset")
        return value

    @model_validator(mode="after")
    def source_identity_matches_record(self):
        url = urlsplit(self.source_url)
        if (url.path != "/sirup/home/detailPaketPenyediaPublic2017/" + self.id_rup
                or url.query or url.fragment):
            raise ValueError("Source locator does not match the planning identifier")
        return self

    def public_view(self):
        row = self.model_dump(mode="json", exclude={"source_url", "retrieved_at", "source_sha256"})
        row.update(
            synthetic=False, classification=None, evidence_status="not_assessed",
            classification_reason="Source observation only. No risk analysis or human-reviewed finding is available.",
            normalized_item=None,
            coverage={key: getattr(self, key) is not None for key in (
                "total_pagu", "description", "spesifikasi_pekerjaan", "volume_pekerjaan", "metode_pemilihan")},
            price_forensics={"status": "not_assessed", "reason": "No verified applicable benchmark has been linked.",
                             "implied_unit_price": None, "benchmark_unit_price": None,
                             "delta_idr": None, "delta_percent": None},
            provenance={"stage": "public_source_capture", "source_id": self.source_sha256,
                        "source_url": self.source_url, "retrieved_at": self.retrieved_at.isoformat(),
                        "sha256": self.source_sha256, "computed": False, "model_asserted": False,
                        "synthetic": False},
            supporting_evidence=[], counterevidence=["Planning data is not proof of execution or payment."],
            linkage={"status": "unavailable", "tender_id": None},
            review_status="source_observation_not_a_finding", dossier_available=False,
        )
        return row


class ObservationSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: int = Field(default=1, ge=1, le=1)
    records: list[PlanningObservation] = Field(max_length=1000)


def load_snapshot(path):
    """A local operator selects the path; HTTP requests cannot select files or URLs."""
    source = Path(path)
    if source.stat().st_size > 10_000_000:
        raise ValueError("Observation snapshot exceeds the local size limit")
    payload = source.read_bytes()
    snapshot = ObservationSnapshot.model_validate(json.loads(payload))
    keys = [(row.id_rup, row.tahun_anggaran) for row in snapshot.records]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate scoped planning observation")
    if any(row.region != "Kabupaten Sukoharjo" or row.tahun_anggaran != 2026 for row in snapshot.records):
        raise ValueError("Snapshot is outside the confirmed Sukoharjo 2026 scope")
    return snapshot.records, hashlib.sha256(payload).hexdigest()
