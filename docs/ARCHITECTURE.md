# Architecture

The first-round system is intentionally small:

```text
VideoBrief
  -> Script
  -> ScenePlan
  -> AssetManifest
  -> EditDecision
  -> RenderReport
```

`pipeline_defs/minimal-video.yaml` owns stage order and formal inputs/outputs. `skills/video/` owns stage-level operating rules. `tools/` is reserved for concrete actions; the v0.1 runner uses FFmpeg directly through a local command boundary. `runs/` stores raw evidence, while `reports/` stores comparisons. `ModelProtocol` and `ScriptedModel` preserve a future provider boundary without making tests depend on a model.

The next architectural additions are intentionally locked behind evidence: capability routing (v0.4), checkpoint/resume (v0.5), QA/repair (v0.6), and cost governance (v0.7).
