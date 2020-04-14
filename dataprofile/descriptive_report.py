"""print or save a report of overall statistics and detailed statistics for a given dataset."""
import sys
from datetime import date
from pathlib import Path
from typing import Optional, Union, Dict, Tuple, List

import pandas as pd
from colorama import Fore, init
from loguru import logger
from tabulate import tabulate

from .collect_stats import get_df_profile, get_a_sample
from .config import DEFAULT_SAMPLE_SIZE, AUTHOR, RANDOM_STATE
from .monitor import monitor_time_memory

init(autoreset=True)
logger.remove()
logger.add(sys.stdout, format="{time:YYYY-MM-DD at HH:mm:ss}|{level}|{message}", level="WARNING")


def _str_format(f_name: str) -> Tuple[str, str]:
    """
    Base on the name of the file to store output, return correct table and line breaker format

    :param f_name: target file name
    :return: table and line breaker format
    """
    if f_name.endswith('.html'):
        table_fmt = 'html'
        line_breaker = '<br>'
    elif f_name.endswith('.md'):
        table_fmt = 'pipe'
        line_breaker = '\n\n'
    else:
        table_fmt = 'psql'
        line_breaker = '\n'
    return table_fmt, line_breaker


def profile_to_str(df_profile: Dict[str, Union[pd.DataFrame, list]],
                   var_per_row: int = 6, table_fmt='psql', line_breaker='\n') -> List[str]:
    """
    Convert all statistics to a list of strings.

    :param df_profile: a dictionary of statistics
    :param var_per_row: number of columns to show on each row
    :param table_fmt: the string format of dataframe
    :param line_breaker:
    :return: a list of strings
    """
    report_str = []
    padding_size, padding_size2 = 90, 50

    report_str.append(' Beginning of report '.center(padding_size, '='))
    report_str.append(
        f"{line_breaker}This following report is created by {AUTHOR} on {date.today():%A, %b %d, %Y}{line_breaker}")

    report_str.append(' Table Statistics '.center(padding_size2, '='))
    report_str.append(
        tabulate(df_profile['table_stats'], headers='keys',
                 tablefmt=table_fmt) if table_fmt != 'html' else df_profile['table_stats'].to_html())
    report_str.append(f'{line_breaker}')

    report_str.append(' Variable Summary '.center(padding_size2, '='))
    report_str.append(tabulate(df_profile['var_summary'], headers='keys',
                               tablefmt=table_fmt) if table_fmt != 'html' else df_profile['var_summary'].to_html())
    report_str.append(f'{line_breaker}')

    report_str.append(' Variable Statistics '.center(padding_size2, '='))
    for key, item in df_profile[f'var_stats'].items():
        report_str.append(f'{line_breaker}{key} variables:')
        for i in range(len(df_profile[f'var_stats'][f'{key}']) // (var_per_row + 1) + 1):
            dt = pd.DataFrame(item).T.iloc[:,
                 i * var_per_row:(i + 1) * var_per_row]
            report_str.append(tabulate(
                dt, headers='keys', tablefmt=table_fmt) if table_fmt != 'html' else dt.to_html())
    report_str.append(f'{line_breaker}')

    if 'conf_matrix' in df_profile:
        logger.info("Getting 'Confusion Matrix' ready...")
        report_str.append(' Confusion Matrix '.center(padding_size2, '='))
        for confusion_matrix in df_profile['conf_matrix']:
            report_str.append(f"row:{confusion_matrix.index.name} - col:{confusion_matrix.columns.name}")
            report_str.append(tabulate(confusion_matrix, headers=confusion_matrix.columns,
                                       showindex=confusion_matrix.index.to_list(),
                                       tablefmt=table_fmt) if table_fmt != 'html' else confusion_matrix.to_html())
    report_str.append(' End of report '.center(padding_size, '='))
    return report_str


def print_report(df_profile, var_per_row) -> None:
    """
    Print report to screen.

    :param df_profile:
    :param var_per_row:
    :return: None
    """
    table_fmt = 'psql'
    line_breaker = '\n'
    report_str = profile_to_str(df_profile, var_per_row, table_fmt, line_breaker)
    print(line_breaker.join(report_str))
    logger.info("Report successfully rendered!")


def save_report(df_profile, var_per_row, report_file: Optional[Union[str, Path]] = None) -> None:
    """
    Save report to the target file.

    :param df_profile:
    :param var_per_row:
    :param report_file:
    :return: None
    """
    table_fmt, line_breaker = _str_format(str(report_file))
    report_str = profile_to_str(df_profile, var_per_row, table_fmt, line_breaker)
    with open(report_file, 'w', encoding="UTF-8") as f:
        f.write(line_breaker.join(report_str) + '\n')
        logger.info(Fore.GREEN + f"report saved to {report_file}")
    logger.info("Report successfully rendered!")


@monitor_time_memory
def render_report(df: pd.DataFrame,
                  sample_size: int = DEFAULT_SAMPLE_SIZE,
                  var_per_row: int = 6,
                  random_state: int = RANDOM_STATE,
                  report_file: Optional[Union[str, Path]] = None,
                  num_works: int = -1):
    if sample_size > 0:
        sample_df = get_a_sample(df, sample_size, random_state)
    else:
        sample_df = df

    df_profile = get_df_profile(sample_df, num_works)
    if report_file:
        save_report(df_profile, var_per_row, report_file)
    else:
        print_report(df_profile, var_per_row)

# @monitor_time_memory
# def render_report(df: pd.DataFrame,
#                   prt_table_stats: bool = True,
#                   prt_var_summary: bool = True,
#                   prt_var_stats: bool = True,
#                   prt_conf_matrix: bool = True,
#                   sample_size: int = DEFAULT_SAMPLE_SIZE,
#                   var_per_row: int = 6,
#                   random_state: int = RANDOM_STATE,
#                   report_file: Optional[Union[str, Path]] = None,
#                   is_return_stats: bool = True,
#                   num_works: int = -1) -> Optional[Dict[str, Union[pd.DataFrame, list]]]:
#     """
#     Print out descriptive analysis report for a given dataset.
#
#     :param df: the target dataset
#     :param prt_table_stats: if print the table statistics
#     :param prt_var_summary: if print the variable summaries
#     :param prt_var_stats: if print the variables statistics
#     :param prt_conf_matrix: if print the confusion matrix for binary variables
#     :param sample_size: Number of rows to sample from the target dataframe
#     :param var_per_row: number of columns of stats to print per row
#     :param random_state: Random seed for the row sampler
#     :param report_file: store the report to a file
#     :param is_return_stats:
#     :param num_works: number of cpu cores for multiprocessing
#     :return: None or a dictionary including all stats
#     """
#     report_str, return_stats = [], {}
#     padding_size, padding_size2 = 90, 50
#     table_fmt, line_breaker = _str_format(str(report_file))
#
#     report_str.append(' Beginning of report '.center(padding_size, '='))
#     report_str.append(
#         f"{line_breaker}This following report is created by {AUTHOR} on {date.today():%A, %b %d, %Y}{line_breaker}")
#
#     if sample_size > 0:
#         sample_df, msg = get_a_sample(df, sample_size, random_state, line_breaker)
#         report_str.append(msg) if msg else None
#     else:
#         sample_df = df
#     var_stats = get_variable_stats(sample_df, num_works)
#
#     try:
#         if prt_table_stats:
#             logger.info("Getting 'Table statistics' ready...")
#             table_stats = get_table_stats(sample_df, var_stats)
#             report_str.append(' Table Statistics '.center(padding_size2, '='))
#             return_stats['table_stats'] = table_stats
#             report_str.append(
#                 tabulate(table_stats, headers='keys',
#                          tablefmt=table_fmt) if table_fmt != 'html' else table_stats.to_html())
#             report_str.append(f'{line_breaker}')
#
#         if prt_var_summary:
#             logger.info("Getting 'Variable Summary' ready...")
#             var_summary = get_var_summary(var_stats)
#             return_stats['var_summary'] = var_summary
#             report_str.append(' Variable Summary '.center(padding_size2, '='))
#             report_str.append(tabulate(var_summary, headers='keys',
#                                        tablefmt=table_fmt) if table_fmt != 'html' else var_summary.to_html())
#             report_str.append(f'{line_breaker}')
#
#         if prt_var_stats:
#             logger.info("Getting 'Variable Statistics' ready...")
#             report_str.append(' Variable Statistics '.center(padding_size2, '='))
#             for key, item in var_stats.items():
#                 logger.debug(f"Extracting statistics for {key} variables...")
#                 report_str.append(f'{line_breaker}{key} variables:')
#                 return_stats[f'var_stats_{key}'] = pd.DataFrame(item).drop(['data_type', 'type'], axis=1).T
#                 for i in range(len(var_stats[key]) // (var_per_row + 1) + 1):
#                     dt = pd.DataFrame(item).drop(['data_type', 'type'], axis=1).T.iloc[:,
#                          i * var_per_row:(i + 1) * var_per_row]
#                     report_str.append(tabulate(
#                         dt, headers='keys', tablefmt=table_fmt) if table_fmt != 'html' else dt.to_html())
#             report_str.append(f'{line_breaker}')
#
#         if prt_conf_matrix:
#             binary_vars = [var.name for var in var_stats['Binary']]
#             if len(binary_vars) > 1:
#                 logger.info("Getting 'Confusion Matrix' ready...")
#                 report_str.append(' Confusion Matrix '.center(padding_size2, '='))
#                 return_stats['conf_matrix'] = []
#                 for a, b in combinations(binary_vars, 2):
#                     logger.debug(f"Calculating confusion matrix of {a} and {b}")
#                     confusion_matrix = pd.crosstab(sample_df[a].astype(str), sample_df[b].astype(str))
#                     return_stats['conf_matrix'].append(confusion_matrix)
#                     report_str.append(f"row:{a} - col:{b}")
#                     report_str.append(tabulate(confusion_matrix, headers=confusion_matrix.columns,
#                                                showindex=confusion_matrix.index.to_list(),
#                                                tablefmt=table_fmt) if table_fmt != 'html' else confusion_matrix.to_html())
#         report_str.append(' End of report '.center(padding_size, '='))
#
#     except Exception as e:
#         logger.exception(Fore.RED + f'{e}\nReport not rendered successfully!', backtrace=False, diagnose=False)
#
#     else:
#         if report_file:
#             with open(report_file, 'w', encoding="UTF-8") as f:
#                 f.write(line_breaker.join(report_str) + '\n')
#                 logger.info(Fore.GREEN + f"report saved to {report_file}")
#         else:
#             print(line_breaker.join(report_str))
#         logger.info("Report successfully rendered!")
#
#     return return_stats if is_return_stats else None
