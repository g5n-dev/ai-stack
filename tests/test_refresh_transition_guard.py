from __future__ import annotations

from pathlib import Path

import pytest

from scripts.refresh_transition_guard import (
    RefreshTransitionError,
    validate_post_transition,
)


def _posts(root: Path, names: list[str]) -> Path:
    root.mkdir(parents=True)
    for name in names:
        (root / name).write_text(f"# {name}\n", encoding="utf-8")
    return root


def test_accepts_non_destructive_bounded_refresh(tmp_path: Path) -> None:
    baseline = _posts(tmp_path / "baseline", [f"post-{i:03}.md" for i in range(100)])
    (baseline / ".gitkeep").write_text("", encoding="utf-8")
    candidate = _posts(
        tmp_path / "candidate",
        [f"post-{i:03}.md" for i in range(100)] + [f"new-{i:03}.md" for i in range(35)],
    )

    report = validate_post_transition(baseline, candidate)

    assert report == {"baseline": 100, "candidate": 135, "added": 35, "removed": 0}


def test_rejects_empty_candidate_and_any_existing_post_deletion(tmp_path: Path) -> None:
    baseline = _posts(tmp_path / "baseline", ["one.md", "two.md"])
    empty = _posts(tmp_path / "empty", [])
    with pytest.raises(RefreshTransitionError, match="non-empty"):
        validate_post_transition(baseline, empty)

    candidate = _posts(tmp_path / "candidate", ["one.md"])
    with pytest.raises(RefreshTransitionError, match="delete existing Posts"):
        validate_post_transition(baseline, candidate)


def test_rejects_more_than_500_or_35_percent_additions(tmp_path: Path) -> None:
    baseline = _posts(tmp_path / "ratio-baseline", [f"p-{i:04}.md" for i in range(100)])
    over_ratio = _posts(
        tmp_path / "over-ratio",
        [f"p-{i:04}.md" for i in range(100)] + [f"n-{i:04}.md" for i in range(36)],
    )
    with pytest.raises(RefreshTransitionError, match="35%"):
        validate_post_transition(baseline, over_ratio)

    large_baseline = _posts(
        tmp_path / "large-baseline", [f"p-{i:04}.md" for i in range(2000)]
    )
    over_absolute = _posts(
        tmp_path / "over-absolute",
        [f"p-{i:04}.md" for i in range(2000)]
        + [f"n-{i:04}.md" for i in range(501)],
    )
    with pytest.raises(RefreshTransitionError, match="500"):
        validate_post_transition(large_baseline, over_absolute)


def test_rejects_symlinks_and_non_markdown_payloads(tmp_path: Path) -> None:
    baseline = _posts(tmp_path / "baseline", ["one.md"])
    candidate = _posts(tmp_path / "candidate", ["one.md"])
    (candidate / "unexpected.json").write_text("{}", encoding="utf-8")
    with pytest.raises(RefreshTransitionError, match="regular Markdown"):
        validate_post_transition(baseline, candidate)

    (candidate / "unexpected.json").unlink()
    (candidate / "link.md").symlink_to(candidate / "one.md")
    with pytest.raises(RefreshTransitionError, match="regular Markdown"):
        validate_post_transition(baseline, candidate)
