import sys
from pathlib import Path
from typing import Optional

import click
import pandas as pd
from colorama import Fore, init
from loguru import logger

from ._config import DEFAULT_SAMPLE_SIZE, LOG_FILE, AUTHOR
from .descriptive_report import render_report

init(autoreset=True)
logger.remove()
logger.add(sys.stdout, format="{time:YYYY-MM-DD at HH:mm:ss}|{level}|{message}", level="INFO")
logger.add(LOG_FILE, format="{time:YYYY-MM-DD at HH:mm:ss} | {name: ^15} | {level} | {message}",
           level="DEBUG", rotation="10 MB")


def _find_csv_file() -> Optional[Path]:
    """
    return the first CSV file found in the current directory
    :return:
    """
    csv_lt = list(Path().glob('*.csv'))
    return csv_lt[0] if csv_lt else None


@click.command()
@click.option('-f', '--file', prompt='target cvs file', required=True, help='cvs format is required',
              default=_find_csv_file(),
              show_default=True)
@click.option('-e', '--encoding', prompt='file encoding type', required=False, help='correct encoding is required',
              default='utf8',
              show_default=True)
@click.option('--sample_size', prompt='How big is your sample size? skip if sampling is not needed', required=False,
              default=DEFAULT_SAMPLE_SIZE,
              show_default=True,
              help='the size of sample in the analysis')
@click.option('--var_per_row', prompt='How many variables to show per row?', required=False, default=6,
              show_default=True,
              help='number of variables to show per row')
@click.option('-t', '--save_report_to_file',
              prompt='file type to store the report, skip if not needed or choose one from',
              required=False, default='', type=click.Choice(['', 'html', 'txt', 'md']),
              show_default=True,
              help='file type (html ,txt, or markdown) to store the report, skip if not needed')
def main(file: str, encoding: str = 'utf8', sample_size: int = DEFAULT_SAMPLE_SIZE, var_per_row: int = 6,
         save_report_to_file: str = '') -> None:
    """

    :param encoding:
    :param file:
    :param sample_size:
    :param var_per_row:
    :param save_report_to_file:
    :return:
    """
    logger.debug(f"{AUTHOR} executed at {Path('.').absolute()}")
    logger.debug(f"input args: {locals()}")
    try:
        logger.info(f"Loading data from {file}...")
        df = pd.read_csv(Path(file), low_memory=False, encoding=encoding)
    except FileNotFoundError:
        logger.error(Fore.RED + "Target file doesn't exist! Profiling stopped!")
    except UnicodeDecodeError:
        logger.error(
            Fore.RED + f"This file is not encoded in {encoding}! Correct encoding is required! Profiling stopped!")
    except Exception as e:
        logger.error(Fore.RED + f"{e}! Profiling stopped!")
    else:
        report_file_name = 'report_' + str(file).split('/')[-1].split('.')[
            0] + '.' + save_report_to_file if save_report_to_file else None
        render_report(df, sample_size=sample_size, var_per_row=var_per_row, report_file=report_file_name)


if __name__ == "__main__":
    main()
