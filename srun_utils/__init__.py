from pathlib import Path

from srun_utils.srun_session import SrunSession


__all__ = ['SrunSession', 'srun', 'init']


def init(
    runs_dir: str | Path,
    time: str,
    job_name: str,
    n_gpus: int,
    n_cpus: int,
    mem: int,
    partition: str,
    logs_dir: str | Path | None,
) -> None:
    global SRUN_SESSION
    SRUN_SESSION = SrunSession(runs_dir, time, job_name, n_gpus, n_cpus, mem, partition, logs_dir)


def srun(command: list[str], interactive: bool = False) -> None:
    global SRUN_SESSION
    SRUN_SESSION.srun(command, interactive)
