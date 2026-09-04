import json
from pathlib import Path

from video_agent.artifacts import validate_artifact
from video_agent.models import make_artifact
from video_agent.pipeline import load_pipeline, stage_names

ROOT = Path(__file__).resolve().parents[1]


def test_artifact_envelope_and_payload_contract():
    artifact = make_artifact("script", "test-run", {"title": "t", "topic": "x", "duration_seconds": 5, "sections": []})
    assert validate_artifact(artifact, "script") == []
    assert validate_artifact({"artifact_type": "script"}, "script")


def test_minimal_pipeline_is_ordered_and_closed():
    manifest = load_pipeline(ROOT / "pipeline_defs/minimal-video.yaml")
    assert stage_names(manifest) == ["idea", "script", "scene_plan", "assets", "edit", "compose"]


def test_fixture_has_required_brief_fields():
    brief = json.loads((ROOT / "fixtures/v01/simple_video_brief.json").read_text())
    assert {"title", "topic", "target_duration", "aspect_ratio", "style"}.issubset(brief)
