from __future__ import annotations

import logging
import os
from pathlib import Path
import tomllib
from .schema import Settings
from ..core.paths import find_upwards

log = logging.getLogger(__name__)

def read_toml(path: Path) -> dict:
    """
    Reads .toml file with its paths and returns a dictionary with its values.

    Args:
        path: Path of the TOML file.

    Returns: Plain dictionary with the key-values of the TOML file.

    """
    if not path or not path.is_file():
        return {}
    with path.open("rb") as f:
        log.info("Reading TOML file: %s", path)
        return tomllib.load(f)


def env_config(prefix="TOT_") -> dict:
    """
    Reads the configuration from the environment and returns it as a nested dictionary of the read subcommands.

    Args:
        prefix: The prefix that the system variables must have to be added to the dictionary.

    Returns:
        Nested dictionary. The first key is the word after the first _ of the name of the system variable in lowercase,
        which represents the subcommand name (run, build...) and the second key is the rest of the name of the system
        variable in lowercase. The value is the value of the property. (e.g., TOT_RUN_ENVIRONMENT=docker -->
        env[RUN][ENVIRONMENT] = docker)

    """
    result: dict = {}
    for k, v in os.environ.items():
        if not k.startswith(prefix):
            continue
        parts = k[len(prefix):].lower().split("_")
        if len(parts) >= 2:
            section, key = parts[0], "_".join(parts[1:])
            result.setdefault(section, {})[key] = v
    return result


def merge(a: dict, b: dict) -> dict:
    """
    Merges two dictionaries by setting the values of the first dictionary a with the values of the second dictionary b
    for all the coinciding keys.
    If the values for the same key in the two dictionaries are also dictionaries, perform recursive call to merge those
    in the same way.

    Args:
        a: The first dictionary to merge.
        b: The second dictionary to merge.

    Returns:
        The merged dictionary.
    """
    out = dict(a)
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = merge(out[k], v)
        else:
            out[k] = v
    return out


def load_settings(explicit_config: Path | None = None) -> Settings:
    """
    Loads settings following the priority:
    1. Environment variables: Variables prefixed with TOT_ENVIRONMENT
    2. /etc/tot/tot.toml
    3. ~/.config/tot/tot.toml
    4. tot.toml from the repository
    5. Explicit config given via arguments

    This behaviour is NOT performed by this function but for completion we must say that settings with priority 6 would
    come from CLI arguments.

    Args:
        explicit_config: Path to a run-specific TOT's TOML configuration file.

    Returns:
        Settings object with the configuration from all subcommands.

    """
    # 1) system env (lowest)
    acc = env_config()

    global_paths = [
        Path("/etc/tot/tot.toml"),  # 2) system-wide global config
        Path(os.path.expanduser("~/.config/tot/tot.toml")),  # 3) user-specific global config
    ]
    for gp in global_paths:
        acc = merge(acc, read_toml(gp))

    # 4) repo config (closest tot.toml up-tree)
    repo_cfg = find_upwards("tot.toml", start=Path.cwd())
    if repo_cfg:
        acc = merge(acc, read_toml(repo_cfg))

    # 5) execution-specific config (highest)
    if explicit_config:
        acc = merge(acc, read_toml(explicit_config))

    return Settings.model_validate(acc)
