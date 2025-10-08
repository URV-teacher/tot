from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence, Literal

EnvName = Literal["host", "docker", "flatpak"]
RunDockerOutputName = Literal["vnc", "host"]

@dataclass
class RunSpec:
    nds: Path
    image: Optional[Path]
    environment: Optional[EnvName]
    docker_screen: Optional[RunDockerOutputName]
    entrypoint: Optional[str]
    debug: bool
    port: int
    passthrough: Sequence[str]
    shell: bool
    dry_run: bool


