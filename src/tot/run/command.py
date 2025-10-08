# src/tot/run/command.py
from __future__ import annotations

import logging
from pathlib import Path

from .service import run, resolve_nds
from .spec import RunSpec
from ..config.schema import Settings
from ..core.exec import ExecOptions
from ..core.logging import setup_logging

log = logging.getLogger("tot.run")

def run_nds_command(
        nds: Path, image: Path, shell: bool, passthrough: list[str], settings: Settings, dry_run: bool = False
) -> None:
    setup_logging(settings.logging.level)
    log.debug("Logger level: " + settings.logging.level)
    nds, assumed = resolve_nds(nds, cwd=Path.cwd())
    spec = RunSpec(
        nds=nds,
        image=(Path(image) if image else None),
        environment=settings.run.environment,
        docker_screen=settings.run.docker_screen,
        entrypoint=settings.run.entrypoint,
        debug=settings.run.debug,
        port=settings.run.port,
        passthrough=passthrough,
        shell=shell,
        dry_run=dry_run
    )
    code = run(spec, ExecOptions(dry_run=dry_run))
    raise SystemExit(code)
