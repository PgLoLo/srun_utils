import datetime
from subprocess import CompletedProcess


def timestamp_str() -> str:
    return f'{datetime.datetime.now():%Y-%m-%d_%H-%M-%S.%f}'


def assert_ret_value(ret_value: CompletedProcess[bytes]):
    assert ret_value.returncode == 0, f'Non-zero return code "{ret_value.returncode}"'
    return ret_value
