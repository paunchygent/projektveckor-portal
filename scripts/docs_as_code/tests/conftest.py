"""Pytest configuration for docs-as-code tests.

Purpose:
    Ensure the repository root is on `sys.path` so docs-as-code modules can be imported
    consistently during test collection.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
