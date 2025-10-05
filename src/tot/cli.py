# src/tot/cli.py
from __future__ import annotations
from typing import List, Optional
from pathlib import Path
import typer
from rich.console import Console

from .config.loader import load_settings
from .config.schema import Settings
from .shared_options import (
    EnvironmentOpt, EntrypointOpt, DebugOpt, PortOpt,
    DryRunOpt, TraceOpt, VerboseOpt, QuietOpt,
)

console = Console()
app = typer.Typer(help="tot – URV corrections workflow CLI", no_args_is_help=True)

@app.callback()
def _global(ctx: typer.Context,
            config: Optional[Path] = typer.Option(None, "--config",
                help="Execution-specific config file (highest file priority)")):
    # Load settings once; DON'T call any command here.
    ctx.obj = {"settings": load_settings(explicit_config=config)}

@app.command("run")
def run_command(
    ctx: typer.Context,
    f: Optional[str] = typer.Option(None, "-f", help="Path to .nds file"),
    d: Optional[str] = typer.Option(None, "-d", help="Directory to search for .nds"),
    image: Optional[str] = typer.Option(None, "--image", help="Path to FAT image"),
    shell: bool = typer.Option(False, "-s", "--shell", is_flag=True,
                               help="Open backend shell (docker only)"),
    passthrough: Optional[List[str]] = typer.Argument(None, help="-- args passed to entrypoint",
                                                      show_default=False),

    # common flags
    environment: EnvironmentOpt = None,
    entrypoint: EntrypointOpt = None,
    debug: DebugOpt = False,
    port: PortOpt = 1000,
    dry_run: DryRunOpt = False,
    trace: TraceOpt = False,
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
    if trace:
        settings.logging.level = "trace"
    elif quiet:
        settings.logging.level = "quiet"
    elif verbose:
        settings.logging.level = "debug"

    run_nds_command(
        f=f, d=d, image=image, shell=shell,
        passthrough=passthrough or [], settings=settings, dry_run=dry_run
    )
