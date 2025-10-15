from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence, Literal

EnvName = Literal["host", "docker"]

@dataclass
class BuildSpec:
    d: Path
    environment: Optional[EnvName]
    entrypoint: Optional[str]
    passthrough: Sequence[str]
    shell: bool
    dry_run: bool


