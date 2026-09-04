#!/usr/bin/env python3
"""Run all first-round experiments in order."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for script, args in (("run_v01.py", []), ("run_v01.py", ["--bad-case"]), ("run_v02.py", []), ("run_v03.py", [])):
    subprocess.run([sys.executable, str(ROOT / "scripts" / script), *args], cwd=ROOT, check=True)
