#!/usr/bin/env python3
"""
Local preflight checks
在真正运行抓取/生成前，把本地缺失前提一次性检查出来。
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from runtime_env import load_project_env


REQUIRED_IMPORTS = [
    "requests",
    "yaml",
    "feedparser",
    "bs4",
    "anthropic",
]


def _status_line(level: str, message: str) -> str:
    icon = {"PASS": "PASS", "WARN": "WARN", "FAIL": "FAIL"}.get(level, level)
    return f"[{icon}] {message}"


def _check_python() -> tuple[str, str]:
    version = sys.version_info
    if version < (3, 11):
        return "FAIL", f"Python 版本过低: {version.major}.{version.minor}.{version.micro}，需要 3.11+"
    return "PASS", f"Python 版本: {version.major}.{version.minor}.{version.micro}"


def _check_required_files() -> list[tuple[str, str]]:
    checks: list[tuple[str, str]] = []
    required = [
        PROJECT_ROOT / "config" / "anthropic.yaml",
        PROJECT_ROOT / "config" / "sources.yaml",
        PROJECT_ROOT / "blog" / "config.toml",
        PROJECT_ROOT / "scripts" / "generate_content.py",
    ]
    for path in required:
        if path.exists():
            checks.append(("PASS", f"存在: {path.relative_to(PROJECT_ROOT)}"))
        else:
            checks.append(("FAIL", f"缺失: {path.relative_to(PROJECT_ROOT)}"))
    return checks


def _check_imports() -> list[tuple[str, str]]:
    checks: list[tuple[str, str]] = []
    for module_name in REQUIRED_IMPORTS:
        try:
            __import__(module_name)
            checks.append(("PASS", f"Python 依赖可导入: {module_name}"))
        except Exception as exc:
            checks.append(("FAIL", f"Python 依赖缺失: {module_name} ({exc})"))
    return checks


def _check_env() -> list[tuple[str, str]]:
    checks: list[tuple[str, str]] = []
    env_path = load_project_env(PROJECT_ROOT)
    if env_path:
        checks.append(("PASS", f"已加载环境文件: {env_path.relative_to(PROJECT_ROOT)}"))
    else:
        checks.append(("WARN", "未找到 .env，本地运行将依赖当前 shell 环境变量"))

    required_envs = ["ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL", "ANTHROPIC_MODEL"]
    for key in required_envs[:2]:
        value = str(os.environ.get(key) or "").strip()
        if value:
            checks.append(("PASS", f"环境变量已配置: {key}"))
        else:
            checks.append(("FAIL", f"环境变量缺失: {key}"))

    base_url = str(os.environ.get("ANTHROPIC_BASE_URL") or "").strip().lower()
    model = str(os.environ.get("ANTHROPIC_MODEL") or "").strip()
    if model:
        checks.append(("PASS", "环境变量已配置: ANTHROPIC_MODEL"))
    elif "minimax" in base_url:
        checks.append(("WARN", "未配置 ANTHROPIC_MODEL，将默认回落到 MiniMax-M2.7-highspeed"))
    else:
        checks.append(("WARN", "未配置 ANTHROPIC_MODEL，将使用客户端默认模型"))

    if "minimax" in base_url and model and not model.lower().startswith("minimax"):
        checks.append(("FAIL", f"MiniMax 后端应使用 MiniMax 模型名，当前是: {model}"))

    searxng = str(os.environ.get("SEARXNG_BASE_URL") or "").strip()
    if searxng:
        checks.append(("PASS", "已配置 SEARXNG_BASE_URL"))
    else:
        checks.append(("WARN", "未配置 SEARXNG_BASE_URL，将回退到公共 SearXNG 实例"))
    return checks


def _check_tools(require_hugo: bool) -> list[tuple[str, str]]:
    checks: list[tuple[str, str]] = []
    hugo_path = shutil.which("hugo")
    if hugo_path:
        checks.append(("PASS", f"Hugo 已安装: {hugo_path}"))
    else:
        checks.append(("FAIL" if require_hugo else "WARN", "未找到 hugo，可先只跑内容生成"))
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description="AI Stack local preflight")
    parser.add_argument("--require-hugo", action="store_true", help="把 Hugo 作为必需项")
    args = parser.parse_args()

    checks: list[tuple[str, str]] = []
    checks.append(_check_python())
    checks.extend(_check_required_files())
    checks.extend(_check_imports())
    checks.extend(_check_env())
    checks.extend(_check_tools(require_hugo=args.require_hugo))

    failures = 0
    warnings = 0
    for level, message in checks:
        print(_status_line(level, message))
        if level == "FAIL":
            failures += 1
        elif level == "WARN":
            warnings += 1

    print("")
    if failures:
        print("本地启动前提未满足。先修复 FAIL 项，再运行 `./scripts/run_local.sh`。")
        return 1

    if warnings:
        print("前置检查通过，但存在 WARN 项。系统可以启动，能力会降级。")
    else:
        print("前置检查通过，可以运行 AI Stack。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
