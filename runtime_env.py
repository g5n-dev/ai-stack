"""
Runtime environment helpers
统一加载项目根目录下的 .env，避免 README 写了 .env 但运行时并不会读取。
"""

from __future__ import annotations

from pathlib import Path
import os
from typing import Optional


def find_project_root(start: Optional[Path] = None) -> Path:
    current = (start or Path(__file__).resolve()).resolve()
    if current.is_file():
        current = current.parent

    for candidate in [current, *current.parents]:
        if (candidate / "requirements.txt").exists() and (candidate / "config").exists():
            return candidate
    return Path(__file__).resolve().parent


def _strip_matching_quotes(value: str) -> str:
    text = str(value or "").strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in {"'", '"'}:
        return text[1:-1]
    return text


def load_project_env(project_root: Optional[Path] = None, *, override: bool = False) -> Optional[Path]:
    root = find_project_root(project_root or Path(__file__).resolve())
    env_path = root / ".env"
    if not env_path.exists():
        return None

    try:
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            if not key:
                continue
            if (not override) and key in os.environ and str(os.environ.get(key) or "").strip():
                continue
            os.environ[key] = _strip_matching_quotes(value)
    except Exception:
        return None

    return env_path
