import uuid
import subprocess
from pathlib import Path


class SrunSession:
    def __init__(self, runs_dir: str | Path, time: str, job_name: str):
        runs_dir = Path(runs_dir).expanduser()
        assert runs_dir.exists(), f'Dirrectory with runs {runs_dir} does not exist'

        self.runs_dir = runs_dir
        self.time = time
        self.job_name = job_name

    def srun(self, command: str) -> None:
        work_folder = self.runs_dir / str(uuid.uuid4())
        work_folder.mkdir()

        subprocess.run(
            [
                'sbatch',
                f'--time={self.time}',
                f'--job-name={self.job_name}',
                '--output=%j.stdout',
                '--error=%j.stderr',
                '--wrap',
                command,
            ],
            cwd=work_folder,
        )
