from pydantic import BaseModel, Field
from typing import Literal, Optional

EnvName = Literal["host", "docker", "flatpak", "bmde"]


class LoggingSettings(BaseModel):
    level: Literal["trace", "debug", "info", "warning", "error", "quiet"] = "info"


class RunSettings(BaseModel):
    environment: Optional[EnvName] = None
    entrypoint: Optional[str] = None
    debug: bool = False
    port: int = 1000
    image: Optional[str] = None


class BuildSettings(BaseModel):
    environment: Optional[EnvName] = None
    entrypoint: Optional[str] = "make"


class GitVpnSettings(BaseModel):
    enabled: bool = True
    username: Optional[str] = None
    password: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None


class GitUserSettings(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class GitAuthSettings(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    host: Optional[str] = None


class GitSettings(BaseModel):
    vpn: GitVpnSettings = GitVpnSettings()
    user: GitUserSettings = GitUserSettings()
    auth: GitAuthSettings = GitAuthSettings()
    environment: Optional[EnvName] = None
    entrypoint: Optional[str] = "git"


class Settings(BaseModel):
    logging: LoggingSettings = LoggingSettings()
    run: RunSettings = RunSettings()
    build: BuildSettings = BuildSettings()
    git: GitSettings = GitSettings()
