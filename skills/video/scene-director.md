# Scene Director Skill

Role: map each script section to one renderable scene.

Rules:

- Preserve section order and IDs.
- Every scene has `scene_id`, `start`, `duration`, `voiceover`, and `asset_id`.
- Cover the entire script duration with no gaps.

Completion: schema-valid `scene_plan` whose scene count equals the script section count.
Common failures: orphan scenes, gaps, overlaps, or an asset reference with no manifest entry.
