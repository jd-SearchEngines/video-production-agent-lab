# OpenMontage Upstream Research

This note records source-based observations from OpenMontage at commit `a06d4c234e436f5a9c5889f2271f4516ef8f6b10`. It intentionally separates an upstream design observation from this lab's implementation.

| Question | Upstream design observed in source | Our v0.1–v0.3 boundary |
|---|---|---|
| Why a manifest? | `pipeline_defs/*.yaml` declares ordered stages, required/optional artifacts, tools, skills, review focus, and success criteria. `lib/pipeline_loader.py` loads and validates these declarations. | `pipeline_defs/minimal-video.yaml` declares six stages, required inputs, produced artifacts, tools, and criteria. `src/video_agent/pipeline.py` validates handoff availability. |
| What does the Stage Director do? | `AGENT_GUIDE.md` and `skills/pipelines/explainer/*-director.md` make the agent read stage-specific instructions before acting; the skill contains stage review and completion guidance. | Four independent Markdown skills define script, scene, asset, and compose rules. The v0.3 runner verifies that these files exist and uses their contracts as the treatment boundary. |
| Pipeline versus Skill | The pipeline is the ordered production shape; skills are instruction layers for how to execute and review a stage. | Same WHAT/ORDER versus HOW distinction, using different names and fixtures. |
| Agent orchestration | `AGENT_GUIDE.md` places the agent in the orchestration loop: select manifest, preflight, read skills, call tools, review, and checkpoint. Python is described as tools plus persistence. | This first round keeps orchestration in small experiment runners because the research question is bounded. No provider API or creative model call is hidden in Python. |
| Tool discovery | `tools/tool_registry.py` imports tool modules, registers `BaseTool` subclasses, reports live status, groups by capability/provider, and exposes fallback lookup. | Not implemented until v0.4. v0.1 uses one explicit local FFmpeg path so the evidence is reproducible. |
| Selector versus Provider | The registry and `BaseTool` metadata distinguish capability, provider, tier, status, dependencies, and fallback; selector tools aggregate provider choices. | Not implemented; no provider is called. |
| Checkpoint and resume | `lib/checkpoint.py` persists stage checkpoints, validates artifact payloads, and resolves stage order from the manifest. `skills/meta/checkpoint-protocol.md` defines the agent-facing protocol. | Not implemented; run directories are evidence records, not resumable production state. This is explicitly v0.5 roadmap. |
| Artifacts as interfaces | `schemas/artifacts/*.schema.json` and `lib/checkpoint.py` make artifacts the typed handoff between stages and validate canonical stage outputs. | `src/video_agent/models.py` adds a common envelope with `artifact_type`, `version`, `run_id`, timestamp, upstream artifacts, and payload; `artifacts.py` validates the first-round contract. |
| Reviewer | `skills/meta/reviewer.md` describes artifact, quality, and production checks before progression/presentation. | v0.1 measures file existence and ffprobe metadata only. Full Video QA is v0.6 and not claimed here. |
| Human approval | The upstream manifests mark approval points such as proposal/script/scene planning, and the guide requires communicating consequential decisions. | Not implemented in the local deterministic experiment. |
| Cost tracker | `tools/cost_tracker.py` records estimate, reserve, reconcile, budget, and approval states. | All cost fields are `null` because there are no provider calls. Cost governance is v0.7 roadmap. |
| Composition | Upstream exposes composition tools and documents FFmpeg/Remotion paths in the architecture and pipeline definitions. | v0.1 uses a minimal FFmpeg concat render, deliberately avoiding a copied composer or Remotion dependency. |

## General versus OpenMontage-specific patterns

General agent patterns: explicit stage contracts, typed artifacts, capability boundaries, persistence, observable failure states, and verification before delivery. OpenMontage-specific choices include its particular AGPL codebase, stage names and skills, broad provider/tool catalog, Remotion integration, support-envelope metadata, and its human-facing production policies. This lab borrows the research questions and generic patterns, not implementation text.

## License impact

OpenMontage is AGPL-3.0. The project was read for research and attribution. No OpenMontage code, fixtures, prompts, artwork, or generated media are copied. This repository contains an original implementation under the MIT license; if that boundary changes, source and license impact must be recorded before publication.
