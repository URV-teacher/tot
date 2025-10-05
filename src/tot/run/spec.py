from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence, Literal

EnvName = Literal["host", "docker", "flatpak", "bmde"]


@dataclass
class RunSpec:
    nds: Path
    image: Optional[Path]
    environment: EnvName
    entrypoint: Optional[str]
    debug: bool
    port: int
    passthrough: Sequence[str]
    shell: bool
