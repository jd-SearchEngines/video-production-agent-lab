# Video Evidence

The current real material supports EP01–EP03 only. Every chapter has a code path, Run ID, result, metric, bad case, screenshot candidate, and takeaway.

| Chapter | Code | Run ID | Result | Metric | Bad case | Screenshot candidate | Takeaway |
|---|---|---|---|---|---|---|---|
| v0.1 Brief to MP4 | `scripts/run_v01.py` | `v01-20260904T193042Z` | PASS; playable `projects/v01-demo/renders/final.mp4` | 15.000s, 1280×720, 30fps, 49,667 bytes | `v01-bad-20260904T193043Z`: missing asset causes FFmpeg failure | ffprobe output beside final MP4 | A coding agent can create a local video deliverable. |
| v0.2 Pipeline | `scripts/run_v02.py`, `src/video_agent/pipeline.py` | `v02-20260904T193146Z` | PASS; six comparison rows | Case C locality: ad-hoc `compose`, pipeline `assets` | Case B missing input; Case C asset failure | CSV rows for Case C | Explicit transitions expose failures earlier. |
| v0.3 Stage Skills | `skills/video/*.md`, `scripts/run_v03.py` | `v03-20260904T193146Z` | PASS; same six fixtures | One Large Prompt 1/6 success; Stage Skills 6/6; mean violations 0.833 vs 0 | baseline hook omission and asset mismatch | per-fixture CSV plus skill files | Skills are useful when they change measurable artifact behavior. |

v0.4–v1.0 have no video evidence in this round and remain roadmap claims.
