import os

from .base import BuildBackend
from ..spec import BuildSpec
from ...core.exec import run_cmd, ExecOptions


class DockerRunner(BuildBackend):
    def is_available(self) -> bool:
        return True  # optionally check docker info

    def run(self, spec: BuildSpec, exec_opts: ExecOptions) -> int:
        entry = []
        if spec.entrypoint:
            entry = ["--entrypoint", str(spec.entrypoint) or "make"]

        if spec.shell:
            entry = ["--entrypoint", "bash"]
        docker_img = "aleixmt/bmde-linux:latest"

        dirname = os.path.basename(spec.d)
        mounts = ["-v", f"{spec.d}:/input/{dirname}:ro"]
        envs = []
        ports = []
        img_opt = ["-C" f"/input/{dirname}"]

        run_args = ["docker", "run", "--rm", "-it", *mounts, *envs, *ports, *entry, docker_img, *img_opt,
                    *spec.passthrough]

        return run_cmd(run_args, exec_opts)
