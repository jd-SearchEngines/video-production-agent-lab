"""Small, serializable artifact models used across the first three versions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Artifact:
    artifact_type: str
    version: str
    run_id: str
    created_at: str
    upstream_artifacts: list[str]
    payload: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "artifact_type": self.artifact_type,
            "version": self.version,
            "run_id": self.run_id,
            "created_at": self.created_at,
            "upstream_artifacts": self.upstream_artifacts,
            "payload": self.payload,
        }


@dataclass
class VideoBrief:
    title: str
    topic: str
    target_duration: int
    aspect_ratio: str
    style: str

    def to_payload(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "topic": self.topic,
            "target_duration": self.target_duration,
            "aspect_ratio": self.aspect_ratio,
            "style": self.style,
        }


def make_artifact(
    artifact_type: str,
    run_id: str,
    payload: Dict[str, Any],
    upstream_artifacts: Optional[Iterable[str]] = None,
) -> Dict[str, Any]:
    return Artifact(
        artifact_type=artifact_type,
        version="0.1",
        run_id=run_id,
        created_at=utc_now(),
        upstream_artifacts=list(upstream_artifacts or []),
        payload=payload,
    ).to_dict()
