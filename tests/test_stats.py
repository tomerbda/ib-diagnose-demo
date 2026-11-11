from pathlib import Path

from cachereport.parser import read_records
from cachereport.stats import summarize

SAMPLE = Path(__file__).resolve().parent.parent / "samples" / "build-2026-11-03.jsonl"


def test_summary_on_sample():
    with SAMPLE.open(encoding="utf-8") as fh:
        s = summarize(read_records(fh))
    assert s.total == 6
    assert s.cacheable == 5
    assert s.hits == 3
    assert round(s.hit_rate, 2) == 0.60
    assert s.saved_ms == (4200 - 180) + (5100 - 210) + (3900 - 150)


def test_slowest_uncached_order():
    with SAMPLE.open(encoding="utf-8") as fh:
        s = summarize(read_records(fh), top=2)
    assert [r.task for r in s.slowest_uncached] == ["link.exe app.exe", "cl.exe net/socket.cpp"]
