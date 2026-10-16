"""Validate a private captured execution snapshot and retain evidence gaps."""
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Literal
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class SourceReference(BaseModel):
    model_config = ConfigDict(extra="forbid")
    stage: str
    source_url: str
    retrieved_at: datetime
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    synthetic: Literal[False]
    computed: Literal[False]
    model_asserted: Literal[False]
    reuse_status: str

    @field_validator("source_url")
    @classmethod
    def validate_locator(cls, value):
        url = urlsplit(value)
        if (url.scheme != "https" or url.netloc != "spse.inaproc.id" or url.query or url.fragment
                or not re.fullmatch(r"/sukoharjokab/(lelang|nontender)/\d{1,20}/(pengumumanlelang|pengumumanpl|peserta)", url.path)):
            raise ValueError("Expected a canonical public Sukoharjo SPSE locator")
        return value

    @field_validator("retrieved_at")
    @classmethod
    def require_timezone(cls, value):
        if value.utcoffset() is None:
            raise ValueError("Source time requires a UTC offset")
        return value


class ObservedParticipant(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(max_length=100)
    nama_peserta: str = Field(max_length=500)
    identity_status: Literal["source_masked", "public_name_only"]
    bid: None = None
    evaluation: None = None
    alasan_gugur: None = None
    bid_to_hps_percent: None = None


class ObservedExecution(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(pattern=r"^\d{1,20}$")
    kode_lelang: str
    kind: Literal["tender", "non_tender"]
    nama_tender: str = Field(min_length=1, max_length=2000)
    satker: str = Field(min_length=1, max_length=500)
    region: Literal["Kab. Sukoharjo"]
    tahun_anggaran: Literal[2026]
    total_pagu: str = Field(pattern=r"^\d{1,29}(?:\.\d{1,2})?$")
    hps: str = Field(pattern=r"^\d{1,29}(?:\.\d{1,2})?$")
    id_rup: str | None
    rup_ids: list[str] = Field(max_length=100)
    linkage_status: Literal["explicit_source_rup", "not_linked"]
    stage: str | None
    participants: list[ObservedParticipant] = Field(max_length=100)
    signals: list[str] = Field(max_length=0)
    nama_pemenang: None = None
    coverage: dict[str, str]
    synthetic: Literal[False]
    provenance: SourceReference
    participant_provenance: SourceReference | None = None
    participant_error: str | None = Field(default=None, max_length=1000)
    capture_manifest: str | None = Field(default=None, pattern=r"^manifest-[a-f0-9]{32}\.json$", exclude=True)

    @model_validator(mode="after")
    def verify_identity(self):
        path = urlsplit(self.provenance.source_url).path
        expected = f"/sukoharjokab/{'lelang' if self.kind == 'tender' else 'nontender'}/{self.id}/"
        announcement = "pengumumanlelang" if self.kind == "tender" else "pengumumanpl"
        if path != expected + announcement or self.kode_lelang != self.id:
            raise ValueError("Execution source identity mismatch")
        if self.participant_provenance and urlsplit(self.participant_provenance.source_url).path != expected + "peserta":
            raise ValueError("Participant source identity mismatch")
        if any(not re.fullmatch(r"\d{1,30}", value) for value in self.rup_ids):
            raise ValueError("Malformed RUP relation")
        if len(set(self.rup_ids)) != len(self.rup_ids) or self.id_rup != (self.rup_ids[0] if len(self.rup_ids) == 1 else None):
            raise ValueError("Ambiguous RUP relation")
        if self.linkage_status != ("explicit_source_rup" if self.rup_ids else "not_linked"):
            raise ValueError("Inconsistent source linkage state")
        if len({row.id for row in self.participants}) != len(self.participants):
            raise ValueError("Duplicate participant observation")
        return self


def load_execution(path):
    source = Path(path)
    if source.stat().st_size > 2_000_000:
        raise ValueError("Execution snapshot exceeds the local size limit")
    return ObservedExecution.model_validate(json.loads(source.read_bytes()))
