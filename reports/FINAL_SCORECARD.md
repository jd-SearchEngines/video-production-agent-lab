# Final Scorecard — First Round

| Version | Experiment | Status | Metric | Evidence | Confidence | Caveat |
|---|---|---|---|---|---|---|
| v0.1 | Minimal Video Agent | PASS | 15.000s, 1280×720, 30fps, 49,667 bytes; cost `null` | `projects/v01-demo/renders/final.mp4`, `runs/v01/v01-20260904T193042Z` | High for local render reproducibility | Text-card animatic; no narration or human quality review |
| v0.1 | Bad case | PASS | Missing asset produced a real non-zero FFmpeg failure | `bad_cases/v01/v01-bad-20260904T193043Z` | High for failure reproduction | Failure is intentionally local and deterministic |
| v0.2 | Ad-hoc vs Pipeline | PASS | Case C failure localized at `compose` vs `assets`; 3 fixtures × 2 modes | `reports/v02_pipeline_comparison.csv`, `runs/v02/v02-20260904T193146Z` | Medium | Lightweight simulation; no latency or human study |
| v0.3 | One Large Prompt vs Stage Skills | PASS | Success 1/6 vs 6/6; mean violations 0.833 vs 0 | `reports/v03_skill_comparison.csv`, `runs/v03/v03-20260904T193146Z` | Medium | Deterministic scripted boundary; no real LLM |
| CI | Contracts and tests | PASS | `5 passed`; Ruff clean | `tests/`, `.github/workflows/ci.yml` | High for current code | CI remote run must be checked after push |

## Publication state

- Repository: `jd-SearchEngines/video-production-agent-lab`
- Branch: `main`
- Final commit: recorded in the final handoff message after push
- Upstream SHA: `a06d4c234e436f5a9c5889f2271f4516ef8f6b10`
- No API keys, secrets, environments, model weights, or large generated media are included.
