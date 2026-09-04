#!/usr/bin/env python3
"""Run the local v0.1 Minimal Video Agent, or its deliberate bad case."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from video_agent.artifacts import validate_artifact
from video_agent.models import make_artifact


def utc_run_id(version: str) -> str:
    return f"{version}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"


def run_command(command: List[str], cwd: Path) -> Tuple[int, str, str]:
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    return completed.returncode, completed.stdout, completed.stderr


def write_json(path: Path, value: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def safe_log(text: str) -> str:
    """Keep evidence portable by removing the local checkout's absolute path."""
    text = text.replace(str(ROOT), "<repo>")
    return re.sub(r"/Users/[^\s']+", "<user-path>", text)


def probe(path: Path) -> Dict[str, Any]:
    command = [
        "ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)
    ]
    completed = subprocess.run(command, text=True, capture_output=True, check=True)
    data = json.loads(completed.stdout)
    stream = next(item for item in data["streams"] if item["codec_type"] == "video")
    return {
        "duration_seconds": float(data["format"]["duration"]),
        "resolution": f"{stream['width']}x{stream['height']}",
        "fps": stream.get("r_frame_rate"),
        "file_size_bytes": path.stat().st_size,
    }


def build_success() -> Path:
    started = time.monotonic()
    run_id = utc_run_id("v01")
    run_dir = ROOT / "runs" / "v01" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    brief = json.loads((ROOT / "fixtures/v01/simple_video_brief.json").read_text(encoding="utf-8"))
    write_json(run_dir / "input.json", make_artifact("video_brief", run_id, brief))

    sections = [
        {"id": "s1", "text": "A brief becomes a plan.", "duration_seconds": 5},
        {"id": "s2", "text": "Tools turn the plan into assets.", "duration_seconds": 5},
        {"id": "s3", "text": "Verification makes the result deliverable.", "duration_seconds": 5},
    ]
    script = make_artifact(
        "script", run_id,
        {"title": brief["title"], "topic": brief["topic"], "duration_seconds": 15, "sections": sections},
        ["video_brief"],
    )
    scenes = [
        {"scene_id": item["id"], "start": i * 5, "duration": 5, "voiceover": item["text"], "asset_id": f"asset_{i+1}"}
        for i, item in enumerate(sections)
    ]
    scene_plan = make_artifact("scene_plan", run_id, {"duration_seconds": 15, "scenes": scenes}, ["script"])
    write_json(run_dir / "script.json", script)
    write_json(run_dir / "scene_plan.json", scene_plan)

    assets_dir = run_dir / "assets"
    assets_dir.mkdir()
    colors = ["#172554", "#14532d", "#581c87"]
    asset_items = []
    stderr_parts = []
    stdout_parts = []
    for i, scene in enumerate(scenes):
        image_file = assets_dir / f"scene_{i+1}.png"
        image = Image.new("RGB", (1280, 720), colors[i])
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
        except OSError:
            font = ImageFont.load_default()
        draw.rectangle((60, 60, 1220, 660), outline=(255, 255, 255), width=4)
        draw.rectangle((90, 570, 1190, 590), fill=(255, 255, 255))
        bbox = draw.multiline_textbbox((0, 0), scene["voiceover"], font=font, spacing=8, align="center")
        text_x = (1280 - (bbox[2] - bbox[0])) / 2
        text_y = (720 - (bbox[3] - bbox[1])) / 2
        draw.multiline_text((text_x, text_y), scene["voiceover"], fill=(255, 255, 255), font=font, spacing=8, align="center")
        image.save(image_file)
        video_file = assets_dir / f"scene_{i+1}.mp4"
        command = [
            "ffmpeg", "-y", "-loop", "1", "-i", str(image_file), "-t", "5", "-r", "30",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", str(video_file),
        ]
        code, stdout, stderr = run_command(command, ROOT)
        stdout_parts.append(stdout)
        stderr_parts.append(stderr)
        if code != 0:
            raise RuntimeError(stderr)
        asset_items.append({"asset_id": f"asset_{i+1}", "scene_id": scene["scene_id"], "path": str(video_file.relative_to(ROOT)), "kind": "video_card"})

    manifest = make_artifact("asset_manifest", run_id, {"assets": asset_items}, ["scene_plan", "script"])
    write_json(run_dir / "asset_manifest.json", manifest)
    concat_file = run_dir / "concat.txt"
    run_relative = run_dir.relative_to(ROOT)
    concat_file.write_text("\n".join(f"file '{Path(item['path']).relative_to(run_relative)}'" for item in asset_items) + "\n", encoding="utf-8")
    final_path = ROOT / "projects/v01-demo/renders/final.mp4"
    final_path.parent.mkdir(parents=True, exist_ok=True)
    command = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c", "copy", "-movflags", "+faststart", str(final_path)]
    write_text = safe_log(" ".join(command)) + "\n"
    (run_dir / "compose_command.txt").write_text(write_text, encoding="utf-8")
    code, stdout, stderr = run_command(command, ROOT)
    stdout_parts.append(stdout)
    stderr_parts.append(stderr)
    (run_dir / "stdout.log").write_text(safe_log("\n".join(stdout_parts)), encoding="utf-8")
    (run_dir / "stderr.log").write_text(safe_log("\n".join(stderr_parts)), encoding="utf-8")
    if code != 0:
        raise RuntimeError(stderr)
    metrics = {"success": True, **probe(final_path), "wall_time": round(time.monotonic() - started, 3), "tool_calls": 4, "cost_usd": None, "run_id": run_id}
    write_json(run_dir / "metrics.json", metrics)
    render_report = make_artifact("render_report", run_id, {"output_path": str(final_path.relative_to(ROOT)), "success": True, "metrics": metrics}, ["asset_manifest"])
    write_json(run_dir / "render_report.json", render_report)
    (run_dir / "run_summary.md").write_text(
        f"# v0.1 Run {run_id}\n\nStatus: PASS\n\nGenerated `{final_path.relative_to(ROOT)}` with {metrics['duration_seconds']:.3f}s duration at {metrics['resolution']}.\n\nCost: null (no provider call).\n",
        encoding="utf-8",
    )
    errors = validate_artifact(script, "script") + validate_artifact(scene_plan, "scene_plan") + validate_artifact(manifest, "asset_manifest")
    if errors:
        raise RuntimeError(f"artifact contract errors: {errors}")
    print(json.dumps(metrics, indent=2))
    return final_path


def build_bad_case() -> None:
    run_id = utc_run_id("v01-bad")
    run_dir = ROOT / "runs" / "v01" / run_id
    bad_dir = ROOT / "bad_cases/v01" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    bad_dir.mkdir(parents=True, exist_ok=True)
    missing = run_dir / "assets" / "missing-scene.mp4"
    concat = run_dir / "concat.txt"
    concat.write_text("file 'assets/missing-scene.mp4'\n", encoding="utf-8")
    command = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(run_dir / "failed.mp4")]
    code, stdout, stderr = run_command(command, ROOT)
    (run_dir / "stdout.log").write_text(safe_log(stdout), encoding="utf-8")
    (run_dir / "stderr.log").write_text(safe_log(stderr), encoding="utf-8")
    write_json(bad_dir / "input.json", {"manifest_asset": str(missing.relative_to(ROOT)), "run_id": run_id})
    (bad_dir / "failure").write_text("compose was attempted with a manifest path that does not exist\n", encoding="utf-8")
    (bad_dir / "error").write_text(safe_log(stderr[-2000:]), encoding="utf-8")
    (bad_dir / "analysis").write_text("The failure is localized to compose input materialization: the asset manifest was not checked for file existence before FFmpeg.\n", encoding="utf-8")
    (bad_dir / "fix").write_text("Validate every manifest path before compose; v0.2 makes assets a formal stage with an explicit success criterion.\n", encoding="utf-8")
    write_json(run_dir / "metrics.json", {"success": False, "exit_code": code, "run_id": run_id, "cost_usd": None})
    print(json.dumps({"success": False, "run_id": run_id, "bad_case_dir": str(bad_dir.relative_to(ROOT))}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bad-case", action="store_true")
    args = parser.parse_args()
    build_bad_case() if args.bad_case else build_success()
