import uuid
import subprocess
from pathlib import Path

from srun_utils.utils import timestamp_str


class SrunSession:
    def __init__(
        self,
        runs_dir: str | Path,
        time: str,
        job_name: str,
        n_gpus: int,
        n_cpus: int,
        mem: int,
        partition: str,
        logs_dir: str | Path | None,
    ):
        runs_dir = Path(runs_dir).expanduser()
        assert runs_dir.exists(), f'Directory with runs "{runs_dir}" does not exist'
        if logs_dir is not None:
            logs_dir = Path(logs_dir).expanduser()
            assert logs_dir.exists(), f'Directory with logs "{logs_dir}" does not exist'

        self.runs_dir = runs_dir
        self.time = time
        self.job_name = job_name
        self.n_gpus = n_gpus
        self.n_cpus = n_cpus
        self.mem = mem
        self.partition = partition
        self.logs_dir = logs_dir

    def srun(self, command: str) -> None:
        work_folder = self.runs_dir / timestamp_str()
        work_folder.mkdir()

        log_dir = self.logs_dir if self.logs_dir is not None else work_folder
        log_dir = log_dir.absolute()

        subprocess.run(
            [
                'sbatch',
                f'--time={self.time}',
                f'--job-name={self.job_name}',
                '-p', self.partition,
                '-G', f'{self.n_gpus}',
                '-c', f'{self.n_cpus}',
                '--mem', f'{self.mem}G',
                f'--output={log_dir}/%j.out',
                f'--error={log_dir}/%j.err',
                '--wrap',
                command,
            ],
            cwd=work_folder,
        )
