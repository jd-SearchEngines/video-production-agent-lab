#!/usr/bin/env python3
"""Run the v0.2 ad-hoc versus explicit-pipeline comparison."""

from __future__ import annotations

import csv
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from video_agent.pipeline import load_pipeline, stage_names


def run_id() -> str:
    return f"v02-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"


def scenario(name: str) -> Dict[str, Any]:
    base = {"title": "Coding Agent Video", "topic": "structured production", "target_duration": 15}
    if name == "B_missing_input":
        base.pop("topic")
    if name == "C_asset_failure":
        base["asset_failure"] = True
    return base


def simulate(case: str, mode: str, root: Path) -> Dict[str, Any]:
    started = time.monotonic()
    brief = scenario(case)
    required = {"title", "topic", "target_duration"}
    stages = stage_names(load_pipeline(ROOT / "pipeline_defs/minimal-video.yaml"))
    missing = sorted(required - set(brief))
    invalid = 0
    completed = 0
    failure_stage = None
    if mode == "pipeline":
        if missing:
            failure_stage = "idea"
            invalid = 1
        else:
            for stage in stages:
                if stage == "assets" and brief.get("asset_failure"):
                    failure_stage = stage
                    break
                completed += 1
    else:
        # The ad-hoc path starts work in a loose sequence and only notices an
        # absent input when the corresponding operation happens.
        loose = ["script", "assets", "compose"]
        if missing:
            failure_stage = "script"
            invalid = 1
            completed = 0
        elif brief.get("asset_failure"):
            failure_stage = "compose"
            completed = 1
            invalid = 1
        else:
            completed = len(loose)
    success = failure_stage is None
    result = {
        "run_id": run_id(),
        "case": case,
        "mode": mode,
        "task_success": success,
        "stage_completion": completed,
        "missing_artifact_count": len(missing) + (1 if case == "C_asset_failure" and not success else 0),
        "invalid_transition_count": invalid,
        "recovery_locality": failure_stage or "none",
        "steps": completed + (1 if failure_stage else 0),
        "wall_time": round(time.monotonic() - started, 6),
        "cost_usd": None,
    }
    return result


def main() -> None:
    rid = run_id()
    out_dir = ROOT / "runs/v02" / rid
    out_dir.mkdir(parents=True, exist_ok=True)
    rows: List[Dict[str, Any]] = []
    for case in ("A_standard", "B_missing_input", "C_asset_failure"):
        for mode in ("adhoc", "pipeline"):
            row = simulate(case, mode, ROOT)
            row["run_id"] = rid
            rows.append(row)
    (out_dir / "results.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    with (ROOT / "reports/v02_pipeline_comparison.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows({key: ("null" if value is None else value) for key, value in row.items()} for row in rows)
    (ROOT / "reports/v02_analysis.md").write_text(
        f"# v0.2 Pipeline Comparison\n\nRun ID: `{rid}`\n\n"
        "The pipeline catches the missing brief field at `idea` and the asset failure at `assets`, "
        "before compose. The ad-hoc path detects the same asset problem at compose. This is a "
        "failure-locality result only; the lightweight simulation does not claim lower wall time.\n",
        encoding="utf-8",
    )
    print(json.dumps({"run_id": rid, "rows": len(rows), "report": "reports/v02_pipeline_comparison.csv"}, indent=2))


if __name__ == "__main__":
    main()
