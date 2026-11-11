"""Read build-agent task logs (JSON Lines)."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Iterator

CACHE_HIT = "hit"
CACHE_MISS = "miss"
CACHE_SKIP = "skip"  # task not cacheable


@dataclass(frozen=True)
class TaskRecord:
    task: str
    agent: str
    agent_ver: str
    cache: str
    duration_ms: int
    est_ms: int
    ts: datetime


def _parse_ts(value: str) -> datetime:
    # Agents write UTC with a trailing Z.
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def parse_line(line: str) -> TaskRecord:
    raw = json.loads(line)
    return TaskRecord(
        task=raw["task"],
        agent=raw.get("agent", "unknown"),
        agent_ver=raw.get("agent_ver", "unknown"),
        cache=raw.get("cache", CACHE_SKIP).strip(),
        duration_ms=int(raw["duration_ms"]),
        est_ms=int(raw.get("est_ms", 0)),
        ts=_parse_ts(raw["ts"]),
    )


def read_records(lines: Iterable[str]) -> Iterator[TaskRecord]:
    for n, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            yield parse_line(line)
        except (KeyError, ValueError) as exc:
            raise ValueError(f"line {n}: {exc}") from exc
