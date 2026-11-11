"""Aggregate cache statistics over task records."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List

from .parser import CACHE_HIT, CACHE_MISS, TaskRecord


@dataclass
class CacheSummary:
    total: int = 0
    cacheable: int = 0
    hits: int = 0
    saved_ms: int = 0
    slowest_uncached: List[TaskRecord] = field(default_factory=list)

    @property
    def hit_rate(self) -> float:
        if self.cacheable == 0:
            return 0.0
        return self.hits / self.cacheable


def _is_hit(rec: TaskRecord) -> bool:
    return rec.cache == CACHE_HIT


def _is_cacheable(rec: TaskRecord) -> bool:
    return rec.cache in (CACHE_HIT, CACHE_MISS)


def summarize(records: Iterable[TaskRecord], top: int = 3) -> CacheSummary:
    s = CacheSummary()
    uncached: List[TaskRecord] = []
    for rec in records:
        s.total += 1
        if _is_cacheable(rec):
            s.cacheable += 1
        if _is_hit(rec):
            s.hits += 1
            s.saved_ms += max(rec.est_ms - rec.duration_ms, 0)
        else:
            uncached.append(rec)
    uncached.sort(key=lambda r: r.duration_ms, reverse=True)
    s.slowest_uncached = uncached[:top]
    return s
