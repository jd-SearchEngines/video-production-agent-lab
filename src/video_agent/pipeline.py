"""Minimal declarative pipeline loader and validator."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml


class PipelineContractError(ValueError):
    pass


def load_pipeline(path: Path) -> Dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        manifest = yaml.safe_load(handle)
    validate_pipeline(manifest)
    return manifest


def validate_pipeline(manifest: Dict[str, Any]) -> None:
    if not isinstance(manifest, dict) or not manifest.get("stages"):
        raise PipelineContractError("pipeline must declare stages")
    names = [stage.get("name") for stage in manifest["stages"]]
    if any(not name for name in names) or len(names) != len(set(names)):
        raise PipelineContractError("stage names must be non-empty and unique")
    produced: set[str] = set(manifest.get("inputs", []))
    for stage in manifest["stages"]:
        required = set(stage.get("required_inputs", []))
        if not required.issubset(produced):
            missing = sorted(required - produced)
            raise PipelineContractError(f"stage {stage['name']} has unavailable inputs: {missing}")
        produces = set(stage.get("produces", []))
        if not produces:
            raise PipelineContractError(f"stage {stage['name']} must produce an artifact")
        produced.update(produces)


def stage_names(manifest: Dict[str, Any]) -> list[str]:
    return [stage["name"] for stage in manifest["stages"]]
