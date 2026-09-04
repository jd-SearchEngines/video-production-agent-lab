"""Artifact contract validation for the v0.1-v0.3 experiment boundary."""

from __future__ import annotations

from typing import Any, Dict, Optional

REQUIRED_PAYLOAD_FIELDS = {
    "video_brief": {"title", "topic", "target_duration", "aspect_ratio", "style"},
    "script": {"title", "topic", "duration_seconds", "sections"},
    "scene_plan": {"duration_seconds", "scenes"},
    "asset_manifest": {"assets"},
    "edit_decision": {"cuts", "duration_seconds"},
    "render_report": {"output_path", "success", "metrics"},
}


def validate_artifact(artifact: Dict[str, Any], expected_type: Optional[str] = None) -> list[str]:
    """Return contract errors; an empty list means the artifact is valid."""
    errors: list[str] = []
    for field in ("artifact_type", "version", "run_id", "created_at", "upstream_artifacts", "payload"):
        if field not in artifact:
            errors.append(f"missing envelope field: {field}")
    if expected_type and artifact.get("artifact_type") != expected_type:
        errors.append(f"expected artifact_type={expected_type!r}")
    payload = artifact.get("payload")
    if not isinstance(payload, dict):
        errors.append("payload must be an object")
        return errors
    artifact_type = artifact.get("artifact_type")
    required = REQUIRED_PAYLOAD_FIELDS.get(artifact_type, set())
    errors.extend(f"missing payload field: {field}" for field in sorted(required - set(payload)))
    return errors
