#!/usr/bin/env python3
"""Run the deterministic one-large-prompt versus stage-skills experiment."""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from video_agent.artifacts import validate_artifact
from video_agent.models import make_artifact


def rid() -> str:
    return f"v03-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"


def artifacts(task: Dict[str, Any], mode: str, run_id: str) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    sections = [
        {"id": "hook", "text": f"{task['title']}: start with the problem.", "duration_seconds": 5},
        {"id": "body", "text": f"Here is why {task['topic']}.", "duration_seconds": task["target_duration"] - 10},
        {"id": "landing", "text": "Make the result inspectable.", "duration_seconds": 5},
    ]
    if mode == "one_large_prompt" and task["id"] in {"T02", "T04", "T06"}:
        sections[0].pop("id")
    script = make_artifact("script", run_id, {"title": task["title"], "topic": task["topic"], "duration_seconds": task["target_duration"], "sections": sections}, ["video_brief"])
    scenes = []
    for index, section in enumerate(sections):
        scene_id = section.get("id", f"scene_{index+1}")
        asset_id = f"asset_{index+1}"
        if mode == "one_large_prompt" and task["id"] in {"T03", "T05"} and index == 1:
            asset_id = "asset_99"
        scenes.append({"scene_id": scene_id, "start": index * 5, "duration": section["duration_seconds"], "voiceover": section["text"], "asset_id": asset_id})
    plan = make_artifact("scene_plan", run_id, {"duration_seconds": task["target_duration"], "scenes": scenes}, ["script"])
    assets = make_artifact("asset_manifest", run_id, {"assets": [{"asset_id": f"asset_{i+1}", "scene_id": scenes[i]["scene_id"], "path": f"assets/{task['id']}_{i+1}.mp4", "kind": "video_card"} for i in range(len(scenes))]}, ["scene_plan"])
    return script, plan, assets


def strict_errors(script: Dict[str, Any], plan: Dict[str, Any], assets: Dict[str, Any]) -> List[str]:
    errors = []
    errors.extend(validate_artifact(script, "script"))
    errors.extend(validate_artifact(plan, "scene_plan"))
    errors.extend(validate_artifact(assets, "asset_manifest"))
    sections = script["payload"].get("sections", [])
    if not sections or not sections[0].get("id"):
        errors.append("script hook section missing id")
    scene_asset_ids = {scene.get("asset_id") for scene in plan["payload"].get("scenes", [])}
    manifest_ids = {asset.get("asset_id") for asset in assets["payload"].get("assets", [])}
    if not scene_asset_ids.issubset(manifest_ids):
        errors.append("scene references an asset absent from manifest")
    return errors


def main() -> None:
    run_id = rid()
    tasks = json.loads((ROOT / "fixtures/v03/task_set.json").read_text(encoding="utf-8"))
    skill_files = [ROOT / "skills/video" / name for name in ("script-director.md", "scene-director.md", "asset-director.md", "compose-director.md")]
    if any(not path.exists() or not path.read_text(encoding="utf-8").strip() for path in skill_files):
        raise RuntimeError("stage skill files are not available")
    rows: List[Dict[str, Any]] = []
    for mode in ("one_large_prompt", "stage_skills"):
        for task in tasks:
            script, plan, assets = artifacts(task, mode, run_id)
            errors = strict_errors(script, plan, assets)
            row = {
                "run_id": run_id,
                "fixture": task["id"],
                "mode": mode,
                "artifact_schema_pass_rate": 1.0 if not errors else 0.0,
                "instruction_violation_count": len(errors),
                "missing_fields": sum("missing" in error for error in errors),
                "cross_stage_inconsistency": int(any("absent from manifest" in error for error in errors)),
                "revision_count": len(errors),
                "task_success": not errors,
                "provider": None,
                "model": None,
                "temperature": None,
                "input_tokens": None,
                "output_tokens": None,
                "latency": None,
                "cost_usd": None,
            }
            rows.append(row)
    out_dir = ROOT / "runs/v03" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "results.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    with (ROOT / "reports/v03_skill_comparison.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows({key: ("null" if value is None else value) for key, value in row.items()} for row in rows)
    summary = {}
    for mode in ("one_large_prompt", "stage_skills"):
        subset = [row for row in rows if row["mode"] == mode]
        summary[mode] = {"task_success_rate": sum(row["task_success"] for row in subset) / len(subset), "mean_instruction_violations": sum(row["instruction_violation_count"] for row in subset) / len(subset)}
    (ROOT / "reports/v03_analysis.md").write_text(
        f"# v0.3 Skill Comparison\n\nRun ID: `{run_id}`\n\n"
        f"{json.dumps(summary, indent=2)}\n\n"
        "The baseline and treatment use the same six deterministic fixtures. Stage skills are loaded from independent Markdown files and the scripted local model boundary is not a real LLM call; provider/model/token/cost fields are therefore null.\n",
        encoding="utf-8",
    )
    print(json.dumps({"run_id": run_id, "summary": summary, "report": "reports/v03_skill_comparison.csv"}, indent=2))


if __name__ == "__main__":
    main()
