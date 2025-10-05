from .base import RunnerBackend
from ..spec import RunSpec
from ...core.exec import run_cmd, ExecOptions


class DockerRunner(RunnerBackend):
    def is_available(self) -> bool:
        return True  # optionally check docker info

    def run(self, spec: RunSpec, exec_opts: ExecOptions) -> int:
        # desmume-docker default entrypoint is desmume-cli
        entry = spec.entrypoint or "desmume-cli"
        docker_img = "aleixmt/desmume-cli:latest"
        mounts = ["-v", f"{spec.nds.parent}:/roms:ro"]
        img_opt = []
        if spec.image:
            mounts += ["-v", f"{spec.image}:/fs/fat.img:ro"]
            img_opt += ["--cflash-image", "/fs/fat.img"]

        debug_opt = ["--gdb-stub", "--arm9gdb-port", str(spec.port)] if spec.debug else []
        run_args = ["docker", "run", "--rm", "-it", *mounts, docker_img, entry, f"/roms/{spec.nds.name}", *img_opt,
                    *debug_opt, *spec.passthrough]
        if spec.shell:
            run_args = ["docker", "run", "--rm", "-it", *mounts, docker_img, "bash"]
        return run_cmd(run_args, exec_opts)
