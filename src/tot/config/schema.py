"""
Defines the schema of settings of the application.
"""
from typing import Literal, Optional, List

from pydantic import BaseModel

class LoggingSettings(BaseModel):
    level: Literal["trace", "info", "quiet"] = "info"


# The possible backends that we have on the submodules
RunEnvName = Literal["host", "docker", "flatpak"]
RunDockerOutputName = Literal["vnc", "host"]

class RunSettings(BaseModel):
    environment: Optional[RunEnvName] = None
    docker_screen: Optional[RunDockerOutputName] = None
    entrypoint: Optional[str] = "desmume"
    logging: LoggingSettings = None
    passthrough: Optional[List[str]] = None

    debug: bool = False
    port: int = 1000
    image: Optional[str] = None


BuildEnvName = Literal["host", "docker"]

class BuildSettings(BaseModel):
    environment: Optional[BuildEnvName] = None
    entrypoint: Optional[str] = "make"
    logging: LoggingSettings = None
    passthrough: Optional[List[str]] = None


class VpnAuthSettings(BaseModel):
    enabled: bool = True
    username: Optional[str] = None
    password: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None


class GitAuthSettings(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    host: Optional[str] = None


class GitConfigSettings(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


GitEnvName = Literal["host", "docker"]

class GitSettings(BaseModel):
    environment: Optional[GitEnvName] = None
    entrypoint: Optional[str] = "git"
    logging: LoggingSettings = None
    passthrough: Optional[List[str]] = None

    vpn_auth: VpnAuthSettings = VpnAuthSettings()
    git_auth: GitAuthSettings = GitAuthSettings()
    git_config: GitConfigSettings = GitConfigSettings()


class Settings(BaseModel):
    logging: LoggingSettings = LoggingSettings()
    run: RunSettings = RunSettings()
    build: BuildSettings = BuildSettings()
    git: GitSettings = GitSettings()
