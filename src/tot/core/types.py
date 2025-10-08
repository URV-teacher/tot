"""
Helpers to parse strings & map log levels.
"""
from __future__ import annotations

import logging
from enum import Enum
from typing import Iterable, List, Optional


class Environment(str, Enum):
    """
    Execution/build environment backends.

    Note:
    - "bmde" is included for future/host-like flows (your Bare Metal Dev Env).
    """
    HOST = "host"
    DOCKER = "docker"
    FLATPAK = "flatpak"
    BMDE = "bmde"

    @classmethod
    def parse(cls, value: Optional[str]) -> Optional["Environment"]:
        """Parse case-insensitively; returns None if value is falsy."""
        if not value:
            return None
        norm = value.strip().lower()
        try:
            return cls(norm)  # Enum accepts the value directly
        except ValueError as exc:
            valid = ", ".join(v.value for v in cls)
            raise ValueError(f"Unknown environment '{value}'. Valid: {valid}") from exc


# Default backend priority when auto-selecting a runner for `tot run`.
# host > docker > flatpak.
DEFAULT_RUN_ENV_PRIORITY: List[Environment] = [
    Environment.HOST,
    Environment.DOCKER,
    Environment.FLATPAK,
]

#: Reasonable default priority for build/patch flows (you can override per module).
DEFAULT_BUILD_ENV_PRIORITY: List[Environment] = [
    Environment.HOST,
    Environment.DOCKER
]


class LogLevel(str, Enum):
    """
    Logical log levels for the CLI.

    Includes a custom TRACE (more verbose than DEBUG) and QUIET
    (suppresses all output beyond CRITICAL).
    """
    TRACE = "trace"
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    QUIET = "quiet"

    @classmethod
    def parse(cls, value: Optional[str]) -> Optional["LogLevel"]:
        """Parse case-insensitively; returns None if value is falsy."""
        if not value:
            return None
        norm = value.strip().lower()
        try:
            return cls(norm)
        except ValueError as exc:
            valid = ", ".join(v.value for v in cls)
            raise ValueError(f"Unknown log level '{value}'. Valid: {valid}") from exc

    def to_logging_level(self) -> int:
        """
        Map to stdlib logging numeric levels.
        - TRACE -> 5 (below DEBUG)
        - QUIET -> logging.CRITICAL + 10 (above CRITICAL)
        """
        if self is LogLevel.TRACE:
            # Register name once; harmless if repeated.
            if logging.getLevelName(5) != "TRACE":
                logging.addLevelName(5, "TRACE")
            return 5
        if self is LogLevel.DEBUG:
            return logging.DEBUG
        if self is LogLevel.INFO:
            return logging.INFO
        if self is LogLevel.WARNING:
            return logging.WARNING
        if self is LogLevel.ERROR:
            return logging.ERROR
        if self is LogLevel.QUIET:
            return logging.CRITICAL + 10
        # Fallback
        return logging.INFO


def choose_first_available(
    requested: Optional[Environment],
    candidates: Iterable[Environment],
    is_available: callable,
) -> Optional[Environment]:
    """
    Utility to pick the first available environment.

    - If `requested` is set, return it if available, else None.
    - Otherwise, return the first env in `candidates` for which `is_available(env)` is True.
    """
    if requested:
        return requested if is_available(requested) else None
    for env in candidates:
        if is_available(env):
            return env
    return None


__all__ = [
    "Environment",
    "LogLevel",
    "DEFAULT_RUN_ENV_PRIORITY",
    "DEFAULT_BUILD_ENV_PRIORITY",
    "choose_first_available",
]
