# src/tot/run/command.py
from __future__ import annotations

import logging
from pathlib import Path

from .service import run
from .spec import BuildSpec
from ..config.schema import Settings
from ..core.exec import ExecOptions
from ..core.logging import setup_logging

log = logging.getLogger("tot.run")

def build_nds_command(
        d: Path, shell: bool, passthrough: list[str], settings: Settings, dry_run: bool = False
) -> None:
    setup_logging(settings.logging.level)
    log.debug("Logger level: " + settings.logging.level)
    #nds, assumed = resolve_nds(nds, cwd=Path.cwd()) TODO solve d for current dir
    spec = BuildSpec(
        d=d,
        environment=settings.build.environment,
        entrypoint=settings.build.entrypoint,
        passthrough=passthrough,
        shell=shell,
        dry_run=dry_run
    )
    code = run(spec, ExecOptions(dry_run=dry_run))
    raise SystemExit(code)
