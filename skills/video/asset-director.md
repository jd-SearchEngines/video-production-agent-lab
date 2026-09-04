# Asset Director Skill

Role: materialize the assets requested by the scene plan using local tools.

Rules:

- Create exactly one asset entry per scene.
- Record a relative path, asset ID, scene ID, and kind.
- Check that every recorded path exists before reporting success.

Completion: schema-valid `asset_manifest` with all paths resolvable on disk.
Common failures: missing files, duplicate IDs, and silently substituted providers.
