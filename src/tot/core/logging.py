# src/tot/core/logging.py
from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from rich.logging import RichHandler


def setup_logging(level: str, log_file: Optional[str | Path] = None) -> None:
    """
    Configure logging for tot.

    - Console: pretty (Rich), threshold set by `level` arg.
    - File (optional): rotating file, always DEBUG+ so you keep full details even in quiet mode.

    `level` accepts:
      - "trace"  -> numeric 5 (below DEBUG)
      - "debug", "info", "warning", "error"
      - "quiet"  -> mutes console (file still logs, if enabled)
    """
    # ---- map console level exactly like your previous version
    if level == "trace":
        console_level = 5
        logging.addLevelName(5, "TRACE")
    elif level == "quiet":
        console_level = logging.CRITICAL + 10  # nothing passes to console
    elif level == "info":
        console_level = getattr(logging, level.upper(), logging.INFO)
    else:
        raise ValueError(f"{level} is not a valid logging level")

    handlers: list[logging.Handler] = []

    # ---- console (Rich)
    console = RichHandler(
        rich_tracebacks=True,
        markup=True,
        show_time=False,
        show_level=True,
        show_path=False,
    )
    console.setLevel(console_level)
    # Rich renders nicely; keep message-only format on console
    console.setFormatter(logging.Formatter("%(message)s"))
    handlers.append(console)

    # ---- optional rotating file
    if log_file:
        path = Path(log_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            path, maxBytes=2_000_000, backupCount=5, encoding="utf-8"
        )
        # Always capture full detail to file
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                "%Y-%m-%d %H:%M:%S",
            )
        )
        handlers.append(file_handler)

    # Root at DEBUG so file handler can see everything; console filtering happens on its own level.
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=handlers,
        format="%(message)s",
        force=True,  # reconfigure cleanly if called again (tests, reloads)
    )