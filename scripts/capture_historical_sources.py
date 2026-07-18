#!/usr/bin/env python3
"""Capture a bounded evidence batch from an offline historical inventory."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ai_stack.historical_capture_job import (  # noqa: E402
    DEFAULT_CONCURRENCY,
    DEFAULT_LIMIT,
    DEFAULT_PER_HOST_CONCURRENCY,
    DEFAULT_TIMEOUT,
    MAX_CONCURRENCY,
    MAX_LIMIT,
    MAX_PER_HOST_CONCURRENCY,
    MAX_TIMEOUT,
    HistoricalCaptureJobError,
    capture_audit_summary,
    load_blog_allowlist,
    load_capture_audit,
    load_historical_capture_inventory,
    run_historical_capture_job,
    write_capture_audit,
)

_SOURCE_CHOICES = (
    "arxiv",
    "github_trending",
    "hacker_news",
    "juejin",
    "blogs_podcasts",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inventory",
        type=Path,
        required=True,
        help="pure-offline historical rehydration inventory JSON",
    )
    parser.add_argument(
        "--source",
        action="append",
        choices=_SOURCE_CHOICES,
        help="exact source filter; repeat for multiple sources",
    )
    parser.add_argument(
        "--filter",
        default="",
        help="case-insensitive substring filter over path, source and canonical URL",
    )
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument(
        "--blog-allowlist-config",
        type=Path,
        help="versioned JSON containing exact public blog hosts",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="explicit mode-0600 evidence audit; omitted means zero local writes",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="reuse successful items from the existing --output audit",
    )
    parser.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)
    parser.add_argument(
        "--per-host-concurrency",
        type=int,
        help="default is min(2, --concurrency)",
    )
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    return parser


def _same_path(left: Path, right: Path) -> bool:
    return left.absolute() == right.absolute()


def _inside_repository(path: Path) -> bool:
    try:
        path.absolute().relative_to(PROJECT_ROOT.absolute())
    except ValueError:
        return False
    return True


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if not 1 <= args.limit <= MAX_LIMIT:
            raise HistoricalCaptureJobError("limit_invalid")
        if not 1 <= args.concurrency <= MAX_CONCURRENCY:
            raise HistoricalCaptureJobError("capture_bounds_invalid")
        if not 1 <= args.timeout <= MAX_TIMEOUT:
            raise HistoricalCaptureJobError("capture_bounds_invalid")
        per_host = args.per_host_concurrency
        if per_host is None:
            per_host = min(DEFAULT_PER_HOST_CONCURRENCY, args.concurrency)
        if not 1 <= per_host <= min(MAX_PER_HOST_CONCURRENCY, args.concurrency):
            raise HistoricalCaptureJobError("capture_bounds_invalid")
        if args.resume and args.output is None:
            raise HistoricalCaptureJobError("resume_requires_output")
        if args.output is not None:
            if _inside_repository(args.output):
                raise HistoricalCaptureJobError(
                    "capture_output_repository_path_rejected"
                )
            if _same_path(args.output, args.inventory):
                raise HistoricalCaptureJobError("capture_output_invalid")
            if args.blog_allowlist_config is not None and _same_path(
                args.output, args.blog_allowlist_config
            ):
                raise HistoricalCaptureJobError("capture_output_invalid")

        inventory = load_historical_capture_inventory(args.inventory)
        allowed_hosts = (
            load_blog_allowlist(args.blog_allowlist_config)
            if args.blog_allowlist_config is not None
            else frozenset()
        )
        resume_audit = (
            load_capture_audit(args.output)
            if args.resume and args.output is not None
            else None
        )
        audit = run_historical_capture_job(
            inventory,
            sources=args.source,
            filter_text=args.filter,
            limit=args.limit,
            blog_allowed_hosts=allowed_hosts,
            concurrency=args.concurrency,
            per_host_concurrency=per_host,
            timeout=args.timeout,
            resume_audit=resume_audit,
        )
        write_performed = args.output is not None
        if args.output is not None:
            write_capture_audit(args.output, audit)
        summary = capture_audit_summary(audit, write_performed=write_performed)
    except (HistoricalCaptureJobError, OSError, ValueError) as exc:
        reason = str(exc) if isinstance(exc, HistoricalCaptureJobError) else "capture_job_failed"
        print(f"historical-capture: rejected: {reason}", file=sys.stderr)
        return 2
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if int(summary.get("failed_count") or 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())
