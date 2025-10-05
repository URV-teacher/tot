from pathlib import Path
from typing import Optional, Iterable


def find_upwards(name: str, start: Path) -> Optional[Path]:
    cur = start.resolve()
    root = cur.anchor
    while True:
        candidate = cur / name
        if candidate.exists():
            return candidate
        if str(cur) == root:
            return None
        cur = cur.parent


def find_first(paths: Iterable[Path], pattern: str) -> Optional[Path]:
    for p in paths:
        for hit in p.glob(pattern):
            return hit
    return None
