import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_v03_fixture_set_is_deterministic_and_bounded():
    tasks = json.loads((ROOT / "fixtures/v03/task_set.json").read_text())
    assert len(tasks) == 6
    assert len({task["id"] for task in tasks}) == 6
    assert all(task["target_duration"] in (15, 20) for task in tasks)


def test_skills_are_independent_files():
    for name in ("script-director.md", "scene-director.md", "asset-director.md", "compose-director.md"):
        content = (ROOT / "skills/video" / name).read_text()
        assert "Completion:" in content
