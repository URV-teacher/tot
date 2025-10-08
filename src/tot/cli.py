# src/tot/cli.py
from __future__ import annotations

import logging
from typing import List, Optional
from pathlib import Path
import typer
from rich.console import Console

from .config.loader import load_settings
from .config.schema import Settings
from .core.logging import setup_logging
from .shared_options import (
    EnvironmentOpt, EntrypointOpt, DebugOpt, PortOpt,
    DryRunOpt, VerboseOpt, QuietOpt, DockerScreenOpt,
)

console = Console()
app = typer.Typer(help="tot – URV corrections workflow CLI", no_args_is_help=True)
log = logging.getLogger("tot.cli")

@app.callback()
def _global(ctx: typer.Context,
            config: Optional[Path] = typer.Option(None, "--config",
                help="Execution-specific config file (highest file priority)")):
    settings = load_settings(explicit_config=config)

    # pick a log file path if you want file logs (optional)
    setup_logging(settings.logging.level, log_file="logs/tot.log")

    # Load settings once; DON'T call any command here.
    ctx.obj = {"settings": load_settings(explicit_config=config)}

@app.command("run")
def run_command(
    ctx: typer.Context,

    nds: Optional[Path] = typer.Argument(
        None,
        exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True,
        help="Path to the .nds binary (optional). If omitted, tot searches the current directory.",
    ),
    image: Optional[Path] = typer.Option(
        None, "--image",
        exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True,
        help="Path to FAT image (optional)",
    ),
    shell: bool = typer.Option(False, "-s", "--shell", is_flag=True,
                               help="Open backend shell (docker only)"),
    passthrough: Optional[List[str]] = typer.Argument(None, help="-- args passed to entrypoint",
                                                      show_default=False),
    docker_screen: Optional[DockerScreenOpt] = typer.Argument(None, help="Selects the method to show the desmume "
                                                                   "screen. "
                                                                   "Can be vnc or host",
                                                      show_default=False),
    # common flags
    environment: EnvironmentOpt = None,
    entrypoint: EntrypointOpt = None,
    debug: DebugOpt = False,
    port: PortOpt = 1000,
    dry_run: DryRunOpt = False,
    verbose: VerboseOpt = False,
    quiet: QuietOpt = False,
):

    """Run an NDS binary via selected backend (host|docker|flatpak)."""
    from .run.command import run_nds_command

    settings: Settings = ctx.obj["settings"]

    # CLI overrides
    if environment is not None:
        settings.run.environment = environment
    if entrypoint is not None:
        settings.run.entrypoint = entrypoint
    if debug:
        settings.run.debug = True
    if port:
        settings.run.port = port
    if quiet:
        settings.logging.level = "quiet"
    if verbose:
        settings.logging.level = "trace"
    if docker_screen:
        settings.run.docker_screen = docker_screen

    # CLI logic
    if entrypoint is not None and shell is True:
        log.warning("The --entrypoint option is incompatible with --shell, entrypoint will be ignored")

    run_nds_command(
        nds=nds, image=image, shell=shell,
        passthrough=passthrough or [], settings=settings, dry_run=dry_run
    )
