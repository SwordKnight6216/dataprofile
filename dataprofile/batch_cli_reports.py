"""Automatically generate reports for all CSV file find in path."""

import os
import sys
from typing import List, Tuple

from loguru import logger

from ._config import LOG_FILE

logger.remove()
logger.add(sys.stdout, format="{time:YYYY-MM-DD at HH:mm:ss}|{level}|{message}", level="INFO")
logger.add(LOG_FILE, format="{time:YYYY-MM-DD at HH:mm:ss} | {name: ^15} | {level} | {message}",
           level="DEBUG", rotation="10 MB")


def _human_readable_size(n_bytes: int) -> str:
    """Convert system output size into human readable output.

    :param n_bytes:
    :return:
    """
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while n_bytes >= 1024 and i < len(units) - 1:
        n_bytes /= 1024.
        i += 1
    f = f"{n_bytes:.2f}"
    return f"{f} {units[i]}"


def find_files(target_dir: str = os.getcwd(), file_suffix: str = ".csv") -> List[Tuple[str, str]]:
    """Find target type of files in target folder and its sub folders.

    :param target_dir:
    :param file_suffix:
    :return:
    """
    output = []
    for subdir, dirs, files in os.walk(target_dir):
        for filename in files:
            filepath = os.path.join(subdir, filename)
            filepath = "." + filepath[len(target_dir):]
            if filepath.endswith(file_suffix):
                f_size = _human_readable_size(os.path.getsize(filepath))
                print(f_size, filepath)
                output.append((f_size, filepath))
    return output
