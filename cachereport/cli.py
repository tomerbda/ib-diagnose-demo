"""Summarize build-cache activity from a build-agent task log."""
from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from .parser import read_records
from .stats import summarize


def _fmt_ms(ms: int) -> str:
    return f"{ms / 1000:.1f}s"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="cachereport", description=__doc__)
    ap.add_argument("log", help="task log in JSON Lines format")
    ap.add_argument("--top", type=int, default=3, help="slowest uncached tasks to list")
    ap.add_argument("--json", action="store_true", help="print JSON instead of text")
    ap.add_argument("--version", action="version", version=f"cachereport {__version__}")
    args = ap.parse_args(argv)

    with open(args.log, encoding="utf-8") as fh:
        summary = summarize(read_records(fh), top=args.top)

    if args.json:
        json.dump(
            {
                "total": summary.total,
                "cacheable": summary.cacheable,
                "hits": summary.hits,
                "hit_rate": round(summary.hit_rate, 4),
                "saved_ms": summary.saved_ms,
                "slowest_uncached": [r.task for r in summary.slowest_uncached],
            },
            sys.stdout,
            indent=2,
        )
        print()
        return 0

    print(f"tasks:      {summary.total}")
    print(f"cacheable:  {summary.cacheable}")
    print(f"cache hits: {summary.hits} ({summary.hit_rate:.1%})")
    print(f"time saved: {_fmt_ms(summary.saved_ms)}")
    print("slowest uncached tasks:")
    for rec in summary.slowest_uncached:
        print(f"  {_fmt_ms(rec.duration_ms):>8}  {rec.task}  [{rec.agent}]")
    return 0
