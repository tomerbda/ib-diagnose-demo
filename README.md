# cachereport

Small CLI that summarizes build-cache activity from build-agent task logs (JSON Lines).

```
python -m cachereport samples/build-2026-11-03.jsonl
python -m cachereport samples/build-2026-11-03.jsonl --top 5 --json
```

Output: total tasks, cache hit rate, time saved by cache hits, and the slowest uncached tasks.

## Log format

One JSON object per line, written by the build agent:

| field         | type   | notes                                   |
|---------------|--------|-----------------------------------------|
| `task`        | string | task name, e.g. `cl.exe foo.cpp`        |
| `agent`       | string | agent host                              |
| `agent_ver`   | string | build-agent version                     |
| `cache`       | string | cache result for the task               |
| `duration_ms` | int    | wall time of the task                   |
| `est_ms`      | int    | estimated uncached time (hits only)     |
| `ts`          | string | ISO-8601 UTC timestamp                  |

## Development

```
python -m pytest -q
```
