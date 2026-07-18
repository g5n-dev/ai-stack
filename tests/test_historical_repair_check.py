from __future__ import annotations

import json
from pathlib import Path

import yaml

from scripts.repair_historical_content import main


def _write_post(root: Path, *, fixed_point: bool) -> None:
    root.mkdir(parents=True, exist_ok=True)
    metadata: dict[str, object] = {
        "title": "历史修复 fixed-point 检查",
        "description": "用于验证只读历史修复检查命令的固定摘要。",
        "date": "2026-07-18T10:00:00+08:00",
        "draft": False,
        "entry_kind": "auto",
        "source": "hacker_news",
        "external_url": "https://example.com/fixed-point",
        "tags": ["AI"],
        "categories": ["AI 工程"],
        "scenarios": ["AI/ML项目"],
    }
    if fixed_point:
        metadata.update(
            {
                "content_mode": "legacy_analysis",
                "publication_tier": "LEGACY",
                "source_provenance": "legacy_no_snapshot",
                "source_support": 0.0,
            }
        )
    frontmatter = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False).rstrip()
    body = "## 历史分析\n\n" + "这是一段结构闭合且可以稳定重复检查的历史分析正文。" * 8
    (root / "post.md").write_text(
        f"---\n{frontmatter}\n---\n\n{body}\n",
        encoding="utf-8",
    )


def test_check_returns_zero_for_a_fixed_point_without_writing(
    tmp_path: Path,
    capsys,
) -> None:
    root = tmp_path / "content/posts"
    _write_post(root, fixed_point=True)
    before = (root / "post.md").read_bytes()

    status = main(["--content-root", str(root), "--check"])
    output = json.loads(capsys.readouterr().out)

    assert status == 0
    assert output == {
        "fixed_point": True,
        "issues": [],
        "plan_digest": output["plan_digest"],
        "planned_changes": 0,
        "schema_version": "historical_repair_check_v1",
    }
    assert (root / "post.md").read_bytes() == before


def test_check_returns_one_and_a_concise_receipt_when_repair_is_pending(
    tmp_path: Path,
    capsys,
) -> None:
    root = tmp_path / "content/posts"
    _write_post(root, fixed_point=False)
    before = (root / "post.md").read_bytes()

    status = main(["--content-root", str(root), "--check"])
    output = json.loads(capsys.readouterr().out)

    assert status == 1
    assert output["schema_version"] == "historical_repair_check_v1"
    assert output["fixed_point"] is False
    assert output["planned_changes"] == 1
    assert output["issues"] == []
    assert (root / "post.md").read_bytes() == before


def test_pr_ci_runs_the_repository_fixed_point_check() -> None:
    root = Path(__file__).resolve().parents[1]
    workflow = (root / ".github/workflows/ci.yml").read_text(encoding="utf-8")

    assert "Verify historical repair fixed point" in workflow
    assert "python3 scripts/repair_historical_content.py --check" in workflow
