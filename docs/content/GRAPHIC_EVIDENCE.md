# Graphic Evidence Contract

## E01

Claim: The local agent produced a real MP4 from a brief.
Why it matters: Establishes the v0.1 deliverable boundary.
Version: v0.1
Source file: `projects/v01-demo/renders/final.mp4`
Run ID: `runs/v01/<successful-run-id>`
Commit: final Git commit recorded in handoff
Metric: success, duration, resolution, file size, wall time
Code path: `scripts/run_v01.py`
Recommended screenshot: FFmpeg output plus `ffprobe` metadata
Bad case: `bad_cases/v01/<bad-run-id>`
Caveat: text-card animatic only

## E02

Claim: Brief, script, scene plan, assets, and render are linked by artifacts.
Why it matters: Shows a complete inspectable chain.
Version: v0.1
Source file: `runs/v01/<successful-run-id>/`
Run ID: successful v0.1 run
Commit: final Git commit recorded in handoff
Metric: artifact contract validation passes
Code path: `src/video_agent/models.py`
Recommended screenshot: JSON files beside the render
Bad case: missing scene input
Caveat: no external model call

## E03

Claim: Ad-hoc execution can discover an asset problem late.
Why it matters: Failure location is part of agent quality.
Version: v0.2
Source file: `reports/v02_pipeline_comparison.csv`
Run ID: v0.2 run directory
Commit: final Git commit recorded in handoff
Metric: `recovery_locality=compose` for ad-hoc Case C
Code path: `scripts/run_v02.py`
Recommended screenshot: Case C rows
Bad case: Case C asset failure
Caveat: deterministic simulation

## E04

Claim: A formal pipeline localizes the same asset problem at the assets stage.
Why it matters: Explicit transitions make failures inspectable earlier.
Version: v0.2
Source file: `reports/v02_pipeline_comparison.csv`
Run ID: v0.2 run directory
Commit: final Git commit recorded in handoff
Metric: `recovery_locality=assets` for pipeline Case C
Code path: `src/video_agent/pipeline.py`
Recommended screenshot: ad-hoc/pipeline locality comparison
Bad case: Case B missing brief field
Caveat: no claim about lower wall time

## E05

Claim: The YAML manifest is a machine-readable production contract.
Why it matters: Stage inputs and outputs are no longer implicit variables.
Version: v0.2
Source file: `pipeline_defs/minimal-video.yaml`
Run ID: pipeline validation run
Commit: final Git commit recorded in handoff
Metric: six ordered stages; every required input is produced upstream
Code path: `src/video_agent/pipeline.py`
Recommended screenshot: manifest and validation test
Bad case: unavailable required input rejected
Caveat: no provider selection yet

## E06

Claim: One large prompt and stage skills are separable experiment treatments.
Why it matters: It tests instruction structure, not code volume.
Version: v0.3
Source file: `reports/v03_skill_comparison.csv`
Run ID: v0.3 run directory
Commit: final Git commit recorded in handoff
Metric: task success and instruction violations across six fixtures
Code path: `scripts/run_v03.py`
Recommended screenshot: aggregate comparison
Bad case: baseline hook omission
Caveat: no real LLM

## E07

Claim: Pipeline, Skill, and Tool have distinct responsibilities.
Why it matters: The separation creates testable interfaces.
Version: v0.3
Source file: `docs/ARCHITECTURE.md`, `skills/video/`, `scripts/run_v01.py`
Run ID: v0.3 run directory
Commit: final Git commit recorded in handoff
Metric: stage skill files loaded; local tool action retained separately
Code path: `src/video_agent/pipeline.py`
Recommended screenshot: three-layer diagram
Bad case: missing skill file fails the runner
Caveat: no dynamic registry

## E08

Claim: Stage skills improve artifact completeness on the fixed task set.
Why it matters: A skill should change measurable behavior, not merely move text.
Version: v0.3
Source file: `reports/v03_skill_comparison.csv`
Run ID: v0.3 run directory
Commit: final Git commit recorded in handoff
Metric: schema pass rate, missing fields, cross-stage inconsistency, revisions
Code path: `src/video_agent/artifacts.py`
Recommended screenshot: per-fixture CSV
Bad case: baseline asset mismatch
Caveat: deterministic and lightweight
