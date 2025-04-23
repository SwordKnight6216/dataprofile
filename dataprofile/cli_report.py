"""CLI module for generating reports."""

import sys
from pathlib import Path
from typing import Optional

import click
import pandas as pd
from colorama import Fore, init
from loguru import logger

from ._config import DEFAULT_SAMPLE_SIZE, LOG_FILE, AUTHOR
from .reporting import render_report

init(autoreset=True)
logger.remove()
logger.add(sys.stdout, format="{time:YYYY-MM-DD at HH:mm:ss}|{level}|{message}", level="INFO")
logger.add(LOG_FILE, format="{time:YYYY-MM-DD at HH:mm:ss} | {name: ^15} | {level} | {message}",
           level="DEBUG", rotation="10 MB")


def _find_csv_file() -> Optional[Path]:
    """Return the first CSV file found in the current directory.

    :return:
    """
    csv_lt = list(Path().glob('*.csv'))
    return csv_lt[0] if csv_lt else None


@click.command()
@click.option('--file', type=click.Path(exists=True, path_type=Path), help='CSV file to profile')
@click.option('--encoding', default='utf-8', help='File encoding')
@click.option('--sample-size', default=DEFAULT_SAMPLE_SIZE, help='Sample size for profiling')
@click.option('--var-per-row', default=6, help='Variables per row in output')
@click.option('--save-report-to-file', is_flag=True, help='Save report to file')
def main(file: Optional[Path], encoding: str, sample_size: int,
         var_per_row: int, save_report_to_file: bool) -> None:
    """Generate profile report for CSV file."""
    try:
        if file is None:
            file = _find_csv_file()
            if file is None:
                raise click.UsageError("No CSV file found in current directory")
        
        logger.info(f"Loading data from {file}")
        df = pd.read_csv(file, low_memory=False, encoding=encoding)
        
        report_file = None
        if save_report_to_file:
            report_file = file.with_name(f"report_{file.stem}.txt")
        
        render_report(df, sample_size, var_per_row, report_file=report_file)
        
    except Exception as e:
        logger.error(f"{Fore.RED}{str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    render_single_file_report()
