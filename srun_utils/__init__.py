from srun_utils.srun_session import SrunSession


__all__ = ['SrunSession', 'srun', 'init']


def init(*args, **kwargs) -> None:
    global SRUN_SESSION
    SRUN_SESSION = SrunSession(*args, **kwargs)


def srun(command: str) -> None:
    global SRUN_SESSION
    SRUN_SESSION.srun(command)
