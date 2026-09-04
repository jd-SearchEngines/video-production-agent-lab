# Compose Director Skill

Role: turn an edit decision and asset manifest into a playable MP4.

Rules:

- Validate all asset paths before invoking FFmpeg.
- Preserve scene order and target duration.
- Record the exact compose command and probe the resulting file.

Completion: `render_report` with output path, success, and measured metrics.
Common failures: bad concat ordering, missing assets, and confusing render completion with video validity.
