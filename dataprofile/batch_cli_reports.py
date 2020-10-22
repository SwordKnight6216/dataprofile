"""Automatically generate reports for all CSV file find in path."""

import os
import sys
from typing import List, Tuple

import pandas as pd
from loguru import logger

from ._config import LOG_FILE
from .reporting import render_report

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


def find_files(target_dir: str = os.getcwd(), file_suffix: str = ".csv") -> List[Tuple[str, int, str]]:
    """Find target type of files in target folder and its sub folders.

    :param target_dir:
    :param file_suffix:
    :return:
    """
    output = []
    for subdir, dirs, files in os.walk(target_dir):
        for filename in files:
            filepath_full = os.path.join(subdir, filename)
            filepath = "." + filepath_full[len(target_dir):]
            if filepath.endswith(file_suffix):
                f_size_original = os.path.getsize(filepath_full)
                f_size = _human_readable_size(f_size_original)
                output.append((f_size, f_size_original, filepath_full))
    return output


def render_reports_for_all(target_dir: str = os.getcwd(), file_suffix: str = ".csv", report_type: str = ".txt"):
    files = find_files(target_dir, file_suffix)
    for f in files:
        print(f)
    text = input(f"Continue to generate reports for the {len(files)} files? Y/N") or "N"
    if text == "Y":
        cnt = 0
        for _, _, f in files:
            try:
                df = pd.read_csv(f)
                report_file = f[:-len(file_suffix)] + report_type
                logger.info(f"\nRender Report for {f}...")
                render_report(df, report_file=report_file)
                cnt += 1
            except UnicodeDecodeError:
                logger.warning(f"{f} skipped due to UnicodeDecodeError!")
        logger.info(f"Summary: {cnt} reports successfully rendered, {len(files) - cnt} failed.")
    else:
        print("Aborted!")
