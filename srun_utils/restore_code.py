import argparse
from pathlib import Path
from subprocess import run

from srun_utils.ssh_runner import GIT_COMMIT_FILE, GIT_PATCH_FILE
from srun_utils.utils import assert_ret_value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('github', type=str)
    parser.add_argument('wandb_run', type=str)
    parser.add_argument('output_dir', type=Path)
    args = parser.parse_args()

    assert_ret_value(run(['git', 'clone', args.github, args.output_dir]))

    import wandb
    with wandb.restore(GIT_COMMIT_FILE, args.wandb_run, args.output_dir) as f:
        checkpoint = f.read().strip()
    wandb.restore(GIT_PATCH_FILE, args.wandb_run, args.output_dir)

    assert_ret_value(run(['git', 'checkout', checkpoint], cwd=args.output_dir))
    assert_ret_value(run(['git', 'apply', GIT_PATCH_FILE], cwd=args.output_dir))


if __name__ == '__main__':
    main()