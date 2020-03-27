"""print or save a report of overall statistics and detailed statistics for a given dataset."""

import sys
from datetime import date
from pathlib import Path
from typing import Optional

import click
import pandas as pd
from tabulate import tabulate

from datareport.config import DEFAULT_SAMPLE_SIZE, AUTHOR, RANDOM_STATE
from datareport.collect_stats import get_variable_stats, get_table_stats, get_a_sample


def print_report(df: pd.DataFrame,
                 prt_table_stats: bool = True,
                 prt_var_summary: bool = True,
                 prt_var_stats: bool = True,
                 sample_size: int = DEFAULT_SAMPLE_SIZE,
                 var_per_row: int = 6,
                 random_state: int = RANDOM_STATE,
                 report_file: str = '') -> None:
    """
    Print out descriptive analysis report for a given dataset.

    :param df: the target dataset
    :param prt_table_stats: if print the table statistics
    :param prt_var_summary: if print the variable summaries
    :param prt_var_stats: if print the variables statistics
    :param prt_corr_stats: if print the correlation table
    :param prt_plots: if print plots
    :param sample_size: Number of rows to sample from the target dataframe
    :param var_per_row: number of columns of stats to print per row
    :param random_state: Random seed for the row sampler
    :param report_file: store the report to a file
    :return: None
    """

    sample_df = get_a_sample(df, sample_size, random_state)

    var_stats = get_variable_stats(sample_df)

    if report_file:
        report_file = _make_report_file(report_file)
        file = open(report_file, 'w', encoding="UTF-8")
    else:
        file = None

    try:
        print('\n============= Beginning of report ============ ', file=file)
        print(f"\nThe following report is created by {AUTHOR} on {date.today()}", file=file)
        if prt_table_stats:
            table_stats = get_table_stats(sample_df, var_stats)
            print('\n============= Table Statistics ============== \n', file=file)
            print(tabulate(pd.DataFrame(pd.Series(table_stats), columns=['count']), headers='keys', tablefmt='psql'),
                  file=file)

        if prt_var_summary:
            type_stats = ['type', 'count', 'distinct_count', 'p_unique', 'n_missing', 'p_missing']
            tmp_df_stats = []
            for key, item in var_stats.items():
                tmp_df_stats.append(pd.DataFrame(item)[type_stats])
            var_summary = pd.concat(tmp_df_stats)
            var_summary.index.name = 'name'
            print('\n============= Variable Summary ============== \n', file=file)
            print(tabulate(var_summary, headers='keys', tablefmt='psql'), file=file)

        if prt_var_stats:
            print('\n============= Variable Statistics =========== ', file=file)
            for key, item in var_stats.items():
                print(f'\n{key} variables: \n', file=file)
                for i in range(len(var_stats[key]) // (var_per_row + 1) + 1):
                    print(tabulate(
                        pd.DataFrame(item).drop('type', axis=1).T.iloc[:, i * var_per_row:(i + 1) * var_per_row],
                        headers='keys', tablefmt='psql'), file=file)

        print(f"report saved to {report_file}") if file else None
        print('\n=============== End of report ============ ', file=file)

    except:
        print('Report not finished successfully!')
    finally:
        file.close() if file else None


def _make_report_file(file: str) -> Path:
    """
    create a file for store the report
    :param file:
    :return: created file
    """
    path = Path(file)
    if not path.exists():
        path.touch()
    return path


def _find_csv_file() -> Optional[Path]:
    """
    return the first CSV file found in the current directory
    :return:
    """
    csv_lt = list(Path().glob('*.csv'))
    return csv_lt[0] if csv_lt else None


@click.command()
@click.option('--path', prompt='cvs file path', required=True, help='cvs format is required',
              default=_find_csv_file(),
              show_default=True)
@click.option('--prt_table_stats', prompt='print table statistics?', required=False, default=True, show_default=True,
              help='wanna see the overall dataset statistics')
@click.option('--prt_var_stats', prompt='print variable statistics?', required=False, default=True, show_default=True,
              help='wanna see the variable statistics')
@click.option('--sample_size', prompt='How big is your sample size?', required=False, default=DEFAULT_SAMPLE_SIZE,
              show_default=True,
              help='the size of sample in the analysis')
@click.option('--var_per_row', prompt='How many variables to show per row?', required=False, default=6,
              show_default=True,
              help='number of variables to show per row')
@click.option('--save_report_to_file', prompt='file to store the report', required=False, default='',
              show_default=True,
              help='file to store the report')
def main(path: str, prt_table_stats: bool = True,
         prt_var_stats: bool = True,
         sample_size: int = DEFAULT_SAMPLE_SIZE,
         var_per_row: int = 6, save_report_to_file: str = '') -> None:
    """

    :param path:
    :param prt_table_stats:
    :param prt_var_stats:
    :param sample_size:
    :param var_per_row:
    :param save_report_to_file:
    :return:
    """
    try:
        df = pd.read_csv(Path(path))
    except FileNotFoundError:
        print("Target file doesn't exist or not CSV format! \nReporting stopped!")
        sys.exit(1)
    print_report(df, prt_table_stats=prt_table_stats, prt_var_stats=prt_var_stats, sample_size=sample_size,
                 var_per_row=var_per_row, report_file=save_report_to_file)


if __name__ == "__main__":
    main()
