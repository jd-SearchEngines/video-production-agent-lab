# Script Director Skill

Role: turn a validated video brief into a short, speakable script.

Rules:

- Preserve the brief topic and title.
- Include a hook, a concrete explanation, and a landing sentence.
- Put every section in `sections` with `id`, `text`, and `duration_seconds`.
- Make section durations sum to `duration_seconds` within one second.

Completion: schema-valid `script` artifact with non-empty sections and a duration.
Common failures: missing hook, duration drift, and introducing a topic not present in the brief.
