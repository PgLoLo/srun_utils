# PG slurm utils

# Example

server-side run script:
```python
# project/srun.py
import time
import srun_utils

def srun_init():
    srun_utils.init(
        '~/assets/projects/PROJECT_NAME/runs',
        '24:00:00',
        PROJECT_NAME,
        1,
        8,
        127,
        'ais-gpu',
        '~/assets/slurm_logs',
    )


def main():
    srun_init()
    for _ in range(1):
        srun_utils.srun([
            'python', '-m', 'project.main', '--config-name', 'gno_imi',
        ])
        time.sleep(.5)


if __name__ == '__main__':
    main()
```

cleint-side run script:
```python
from pathlib import Path

from srun_utils.ssh_runner import SshRunner


def main():
    SshRunner(
        Path(__file__).parent,  # project root that will be synced to remote server
        '~/assets/sync_srcs',
        'zhores',
        'ml_run',
        [
            'docker',
            'notebooks',
        ]
    ).run('python -m project.srun')


if __name__ == '__main__':
    main()
```
