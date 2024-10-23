import os
from typing import TypeVar

BYTES_IN_A_MEGABYTE = 1048576
T = TypeVar('T')


def getenv_multy(
    *envs,
    default: T = None,
    prefix: str = '',
) -> str | T | None:
    for env in envs:
        if val := getenv(env, prefix=prefix):
            return val
    return default


def getenv_bool(env: str, default: bool = False, prefix: str = '') -> bool:
    val = getenv(env, prefix=prefix)
    return default if val is None else val.lower() == 'true'


def getenv(env, default: T = None, prefix: str = '') -> str | T | None:
    return os.getenv(f'{prefix}_{env}' if prefix else env) or default


def convert_megabytes_to_bytes(size) -> int:
    return int(BYTES_IN_A_MEGABYTE * float(size))
