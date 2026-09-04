# Video Production Agent Lab

## Research Question

What capabilities let a coding agent progress from writing code to independently completing a video-production task?

This repository is a small, evidence-first experiment. It is not production-ready, an industry-grade system, or a full OpenMontage reproduction.

## Why This Project Exists

Video production is a useful stress test for agent orchestration: the work crosses structured creative decisions, files, external tools, and a binary deliverable. The first round asks three bounded questions:

1. Can a local agent turn a brief into a playable MP4 (v0.1)?
2. Does an explicit stage contract make failures easier to locate than ad-hoc execution (v0.2)?
3. Do stage-specific skills improve artifact completeness and consistency over one large prompt (v0.3)?

## Upstream Inspiration

The upstream research target is [GuyRonnen/openmontage](https://github.com/GuyRonnen/openmontage), inspected at commit `a06d4c234e436f5a9c5889f2271f4516ef8f6b10` on 2026-09-05. It is AGPL-3.0. See [docs/UPSTREAM_VERSION.md](docs/UPSTREAM_VERSION.md) and [docs/UPSTREAM_RESEARCH.md](docs/UPSTREAM_RESEARCH.md). This lab independently reimplements only small, generic mechanisms.

## Architecture

`VideoBrief -> Script -> ScenePlan -> AssetManifest -> EditDecision -> RenderReport` is the artifact chain. The v0.2 manifest defines WHAT and ORDER; v0.3 stage skills define HOW; local tools perform ACTION. The model boundary is represented by a `ModelProtocol`, with `ScriptedModel` used for deterministic experiments.

## Version Evolution

- **v0.1 Minimal Video Agent:** local text-card assets, FFmpeg composition, metrics, and a real bad case.
- **v0.2 Pipeline Agent:** explicit YAML stages and an ad-hoc versus pipeline comparison.
- **v0.3 Skill-driven Agent:** independent stage skills and a deterministic one-large-prompt versus stage-skills comparison.
- **v0.4–v1.0:** roadmap only; Tool Registry, checkpoint/resume, QA/repair, cost governance, and approval/audit integration are not implemented in this round.

## Reproduction

```bash
python3 scripts/run_v01.py
python3 scripts/run_v01.py --bad-case
python3 scripts/run_v02.py
python3 scripts/run_v03.py
python3 scripts/run_all.py
python3 -m pytest -q
```

The main v0.1 output is [projects/v01-demo/renders/final.mp4](projects/v01-demo/renders/final.mp4). Run artifacts are under `runs/`; reports are under `reports/`.

## Evidence and Limitations

Evidence entries E01–E08 are in [docs/content/GRAPHIC_EVIDENCE.md](docs/content/GRAPHIC_EVIDENCE.md). The content plan is [docs/content/SERIES_PLAN.md](docs/content/SERIES_PLAN.md), and the video evidence map is [docs/content/VIDEO_EVIDENCE.md](docs/content/VIDEO_EVIDENCE.md). Metrics are local and deterministic, not human-quality, CTR/CVR, or production-readiness evidence. Missing model/cost data is represented as `null`, not zero.

## Upstream Attribution

OpenMontage is an AGPL-3.0 upstream research object. No OpenMontage source files are copied into this repository. Our implementation, fixtures, naming, and experiments are original to this lab. See the attribution documents for the exact inspected files and design boundary.
