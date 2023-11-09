import subprocess
from pathlib import Path

from srun_utils.utils import assert_ret_value, timestamp_str


class SshRunner:
    def __init__(
        self, rsync_from: str | Path, rsync_to: str | Path, host: str, mamba_env: str, to_exclude: list[str],
    ):
        # assert (rsync_from is None) == (rsync_to is None), \
        #     'Either both rsync from and to should be None, orr neither'
        # if rsync_from is not None:
        rsync_from = Path(rsync_from)
        rsync_to = Path(rsync_to)

        self.rsync_from = rsync_from
        self.rsync_to = rsync_to
        self.host = host
        self.mamba_env = mamba_env
        self.to_exclude = to_exclude

    def run(self, command: str):
        try:
            assert_ret_value(subprocess.run(['git', 'add', '-A']))
            with open(self.rsync_from / 'git.commit.txt', 'w') as f:
                assert_ret_value(subprocess.run(['git', 'rev-parse', 'HEAD'], stdout=f))
            with open(self.rsync_from / 'git.patch', 'w') as f:
                assert_ret_value(subprocess.run(['git', 'diff', '--cached'], stdout=f))

            src_folder = self.rsync_to / timestamp_str()
            to_exclude = [f'--exclude={name}' for name in self.to_exclude]
            assert_ret_value(subprocess.run(['rsync', '-az', *to_exclude, f'{self.rsync_from}/', f'{self.host}:{src_folder}']))
            assert_ret_value(subprocess.run([
                'ssh', self.host, f"mamba activate {self.mamba_env}; export PYTHONPATH={src_folder}/; echo $PYTHONPATH; {command}"
            ]))
        finally:
            (self.rsync_from / 'git.commit.txt').unlink(missing_ok=True)
            (self.rsync_from / 'git.patch').unlink(missing_ok=True)
