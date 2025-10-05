from __future__ import annotations

import logging
from pathlib import Path

from .backends.docker import DockerRunner
from .backends.flatpak import FlatpakRunner
from .backends.host import HostRunner
from .spec import RunSpec
from ..core.exec import ExecOptions
from ..core.paths import find_first

log = logging.getLogger(__name__)


def choose_backend(env: str | None) -> list:
    order = ["host", "docker", "flatpak"]
    if env:
        order = [env]  # force
    mapping = {"host": HostRunner(), "docker": DockerRunner(), "flatpak": FlatpakRunner()}
    return [mapping[e] for e in order]


def discover_nds(f: str | None, d: str | None) -> tuple[Path, bool]:
    if f and d:
        raise ValueError("-f and -d are mutually exclusive")
    if f:
        p = Path(f)
        if not p.is_file() or p.suffix.lower() != ".nds":
            log.warning("Provided NDS rom via -f does not have .nds extension.")
        return p, False
    search_dir = Path(d) if d else Path.cwd()
    hit = find_first([search_dir], "*.nds")
    if not hit:
        raise FileNotFoundError("No .nds file found")
    # You can add a ‘warn if multiple’ behavior later
    return hit, True


def run(spec: RunSpec, exec_opts: ExecOptions) -> int:
    for backend in choose_backend(spec.environment):
        if backend.is_available():
            return backend.run(spec, exec_opts)
    raise RuntimeError("No suitable backend available")
