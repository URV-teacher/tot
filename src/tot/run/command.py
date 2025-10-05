# src/tot/run/command.py
from __future__ import annotations
from pathlib import Path
from .service import run as run_service, discover_nds
from .spec import RunSpec
from ..core.exec import ExecOptions
from ..core.logging import setup_logging
from ..config.schema import Settings


def run_nds_command(
        f, d, image, shell, passthrough, settings: Settings, dry_run: bool = False
) -> None:
    setup_logging(settings.logging.level)
    nds, _assumed = discover_nds(f, d)
    spec = RunSpec(
        nds=nds,
        image=(Path(image) if image else None),
        environment=settings.run.environment,
        entrypoint=settings.run.entrypoint,
        debug=settings.run.debug,
        port=settings.run.port,
        passthrough=passthrough,
        shell=shell,
    )
    code = run_service(spec, ExecOptions(dry_run=dry_run))
    raise SystemExit(code)
