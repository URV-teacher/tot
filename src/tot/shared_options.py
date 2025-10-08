# src/tot/shared_options.py
from __future__ import annotations

from pathlib import Path
from typing import Optional
from typing_extensions import Annotated
import typer

# Reusable option aliases (case-insensitive env name)
EnvironmentOpt = Annotated[
    Optional[str],
    typer.Option(
        "-e",
        "--environment",
        help="Backend environment: host|docker|flatpak",
        case_sensitive=False,
    ),
]

EntrypointOpt = Annotated[
    Optional[Path],
    typer.Option(
        "--entrypoint",
        help="Override backend entrypoint executable",
    ),
]

DebugOpt = Annotated[
    bool,
    typer.Option(
        "--debug",
        help="Enable GDB stub if supported",
        is_flag=True,
    ),
]

PortOpt = Annotated[
    int,
    typer.Option(
        "-p",
        "--port",
        help="Debug port (implies --debug)",
    ),
]

DryRunOpt = Annotated[
    bool,
    typer.Option(
        "--dry-run",
        help="Simulate actions without executing",
        is_flag=True,
    ),
]

VerboseOpt = Annotated[
    bool,
    typer.Option(
        "-v",
        "--verbose",
        help="Verbose output",
        is_flag=True,
    ),
]

QuietOpt = Annotated[
    bool,
    typer.Option(
        "-q",
        "--quiet",
        help="Quiet mode (minimal output)",
        is_flag=True,
    ),
]

DockerScreenOpt = Annotated[
    Optional[str],
    typer.Option(
        "-s",
        "--screen",
        help="Method to show the screen when using the \"docker\" environment",
        is_flag=True,
    ),
]

__all__ = [
    "EnvironmentOpt",
    "EntrypointOpt",
    "DebugOpt",
    "PortOpt",
    "DryRunOpt",
    "VerboseOpt",
    "QuietOpt",
    "DockerScreenOpt"
]
