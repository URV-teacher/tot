from __future__ import annotations
from abc import ABC, abstractmethod
from ..spec import RunSpec
from ...core.exec import ExecOptions


class RunnerBackend(ABC):
    @abstractmethod
    def is_available(self) -> bool: ...

    @abstractmethod
    def run(self, spec: RunSpec, exec_opts: ExecOptions) -> int: ...
