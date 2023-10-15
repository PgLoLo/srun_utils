from pathlib import Path

from spm_utils.srun_session import SrunSession


__all__ = ['SrunSession', 'srun', 'init']


def init(runs_dir: Path, time: str, job_name: str) -> None:
    global SRUN_SESSION
    SRUN_SESSION = SrunSession(runs_dir, time, job_name)


def srun(command: str) -> None:
    global SRUN_SESSION
    SRUN_SESSION.srun(command)
