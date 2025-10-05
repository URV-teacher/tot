from __future__ import annotations
import os
from pathlib import Path
import tomllib
from .schema import Settings
from ..core.paths import find_upwards


def read_toml(path: Path) -> dict:
    if not path or not path.is_file():
        return {}
    with path.open("rb") as f:
        return tomllib.load(f)


def env_config(prefix="TOT_") -> dict:
    # Flattened env → nested dict (e.g., TOT_RUN_ENVIRONMENT=docker)
    result: dict = {}
    for k, v in os.environ.items():
        if not k.startswith(prefix):
            continue
        parts = k[len(prefix):].lower().split("_")
        # simple two-level mapping: e.g., run_environment → settings["run"]["environment"]
        if len(parts) >= 2:
            section, key = parts[0], "_".join(parts[1:])
            result.setdefault(section, {})[key] = v
    return result


def merge(a: dict, b: dict) -> dict:
    out = dict(a)
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = merge(out[k], v)
        else:
            out[k] = v
    return out


def load_settings(explicit_config: Path | None = None) -> Settings:
    # 1) system env (lowest)
    acc = env_config()

    # 2) global config
    global_paths = [
        Path("/etc/tot/tot.toml"),
        Path(os.path.expanduser("~/.config/tot/tot.toml")),
    ]
    for gp in global_paths:
        acc = merge(acc, read_toml(gp))

    # 3) repo config (closest tot.toml up-tree)
    repo_cfg = find_upwards("tot.toml", start=Path.cwd())
    if repo_cfg:
        acc = merge(acc, read_toml(repo_cfg))

    # 4) execution-specific config (highest)
    if explicit_config:
        acc = merge(acc, read_toml(explicit_config))

    return Settings.model_validate(acc)
