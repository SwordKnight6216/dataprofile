from pathlib import Path
from typing import Optional

import click
import pandas as pd

from datareport.config import DEFAULT_SAMPLE_SIZE
from datareport.descriptive_report import render_report


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
@click.option('--prt_table_stats', prompt='print table statistics?', required=False, default='y', show_default=True,
              type=click.Choice(['y', 'n']), help='wanna see the overall dataset statistics')
@click.option('--prt_var_summary', prompt='print variable summary?', required=False, default='y', show_default=True,
              type=click.Choice(['y', 'n']),
              help='wanna see the variable summary')
@click.option('--prt_var_stats', prompt='print variable statistics?', required=False, default='y', show_default=True,
              type=click.Choice(['y', 'n']),
              help='wanna see the variable statistics')
@click.option('--prt_conf_matrix', prompt='print confusion matrix for binary variables?', required=False, default='y',
              show_default=True,
              type=click.Choice(['y', 'n']),
              help='wanna see the confusion matrix for binary variables')
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
def main(file: str, prt_table_stats: bool = True, prt_var_summary: bool = True,
         prt_var_stats: bool = True, prt_conf_matrix: bool = True,
         sample_size: int = DEFAULT_SAMPLE_SIZE,
         var_per_row: int = 6, save_report_to_file: str = '') -> None:
    """

    :param file:
    :param prt_table_stats:
    :param prt_var_summary:
    :param prt_var_stats:
    :param prt_conf_matrix:
    :param sample_size:
    :param var_per_row:
    :param save_report_to_file:
    :return:
    """
    try:
        df = pd.read_csv(Path(file), low_memory=False)
    except FileNotFoundError:
        print("\nTarget file doesn't exist!\nReporting stopped!")
    except UnicodeDecodeError:
        print("\nTarget file is not encoded appropriately! \nReporting stopped!")
    except Exception as e:
        print(f"{e} \nReporting stopped!")
    else:
        report_file_name = 'report_' + str(file).split('/')[-1].split('.')[
            0] + '.' + save_report_to_file if save_report_to_file else None
        render_report(df, prt_table_stats=prt_table_stats == 'y', prt_var_summary=prt_var_summary == 'y',
                      prt_var_stats=prt_var_stats == 'y', prt_conf_matrix=prt_conf_matrix == 'y',
                      sample_size=sample_size,
                      var_per_row=var_per_row, report_file=report_file_name, is_return_stats=False)


if __name__ == "__main__":
    main()
