# Experiment Protocol

1. Record a unique Run ID for every invocation.
2. Keep the fixture set fixed within a comparison.
3. Separate deterministic local evidence from real model/provider evidence.
4. Preserve both successful and failed outputs, including stderr for failures.
5. Use `null` for unavailable provider, token, latency, or cost fields.
6. Report the measured result even when it does not support the expected hypothesis.
7. Keep v0.4–v1.0 disabled until v0.1–v0.3 have real evidence.
