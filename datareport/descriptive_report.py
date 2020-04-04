"""print or save a report of overall statistics and detailed statistics for a given dataset."""

from datetime import date
from itertools import combinations
from pathlib import Path, PurePath
from typing import Optional, Union, Dict

import pandas as pd
from tabulate import tabulate

from datareport.collect_stats import get_variable_stats, get_table_stats, get_a_sample, get_var_summary
from datareport.config import DEFAULT_SAMPLE_SIZE, AUTHOR, RANDOM_STATE
from scripts import monitor_time_memory


@monitor_time_memory
def render_report(df: pd.DataFrame,
                  prt_table_stats: bool = True,
                  prt_var_summary: bool = True,
                  prt_var_stats: bool = True,
                  prt_conf_matrix: bool = True,
                  sample_size: int = DEFAULT_SAMPLE_SIZE,
                  var_per_row: int = 6,
                  random_state: int = RANDOM_STATE,
                  report_file: Optional[Union[str, Path]] = None,
                  is_return_stats: bool = True) -> Optional[Dict[str, Union[pd.DataFrame, list]]]:
    """
    Print out descriptive analysis report for a given dataset.

    :param df: the target dataset
    :param prt_table_stats: if print the table statistics
    :param prt_var_summary: if print the variable summaries
    :param prt_var_stats: if print the variables statistics
    :param prt_conf_matrix: if print the confusion matrix for binary varilables
    :param sample_size: Number of rows to sample from the target dataframe
    :param var_per_row: number of columns of stats to print per row
    :param random_state: Random seed for the row sampler
    :param report_file: store the report to a file
    :param is_return_stats:
    :return: None or a dictionary including all stats
    """
    report_str = []
    return_stats = {}
    table_fmt = 'psql'
    line_breaker = '\n'
    padding_size, padding_size2 = 90, 50

    if report_file:
        fmt = PurePath(report_file).suffix.split('.')[-1]
        if fmt == 'html':
            table_fmt = 'html'
            line_breaker = '<br>'
        elif fmt == 'md':
            table_fmt = 'pipe'
            line_breaker = '\n\n'
        file = open(report_file, 'w', encoding="UTF-8")
    else:
        file = None

    report_str.append(' Beginning of report '.center(padding_size, '='))
    report_str.append(
        f"{line_breaker}This following report is created by {AUTHOR} on {date.today():%A, %b %d, %Y}{line_breaker}")

    sample_df = get_a_sample(df, sample_size, random_state, file, line_breaker) if sample_size > 0 else df
    var_stats = get_variable_stats(sample_df)

    try:
        if prt_table_stats:
            table_stats = get_table_stats(sample_df, var_stats)
            report_str.append(' Table Statistics '.center(padding_size2, '='))
            dt = pd.DataFrame(pd.Series(table_stats), columns=['count'])
            return_stats['table_stats'] = dt
            report_str.append(
                tabulate(dt, headers='keys', tablefmt=table_fmt) if table_fmt != 'html' else dt.to_html())
            report_str.append(f'{line_breaker}')

        if prt_var_summary:
            var_summary = get_var_summary(var_stats)
            return_stats['var_summary'] = var_summary
            report_str.append(' Variable Summary '.center(padding_size2, '='))
            report_str.append(tabulate(var_summary, headers='keys',
                                   tablefmt=table_fmt) if table_fmt != 'html' else var_summary.to_html())
            report_str.append(f'{line_breaker}')

        if prt_var_stats:
            report_str.append(' Variable Statistics '.center(padding_size2, '='))
            for key, item in var_stats.items():
                report_str.append(f'{line_breaker}{key} variables:')
                return_stats[f'var_stats_{key}'] = pd.DataFrame(item).drop(['data_type', 'type'], axis=1).T
                for i in range(len(var_stats[key]) // (var_per_row + 1) + 1):
                    dt = pd.DataFrame(item).drop(['data_type', 'type'], axis=1).T.iloc[:,
                         i * var_per_row:(i + 1) * var_per_row]
                    report_str.append(tabulate(
                        dt, headers='keys', tablefmt=table_fmt) if table_fmt != 'html' else dt.to_html())
            report_str.append(f'{line_breaker}')

        if prt_conf_matrix:
            binary_vars = [var.name for var in var_stats['Binary']]
            if len(binary_vars) > 1:
                report_str.append(' Confusion Matrix '.center(padding_size2, '='))
                return_stats['conf_matrix'] = []
                for a, b in combinations(binary_vars, 2):
                    confusion_matrix = pd.crosstab(sample_df[a], sample_df[b])
                    return_stats['conf_matrix'].append(confusion_matrix)
                    report_str.append(f"row:{a} - col:{b}")
                    report_str.append(tabulate(confusion_matrix, headers=confusion_matrix.columns,
                                           showindex=confusion_matrix.index.to_list(),
                                           tablefmt=table_fmt) if table_fmt != 'html' else confusion_matrix.to_html())
        report_str.append(' End of report '.center(padding_size, '='))

    except Exception as e:
        print(f'{e}\nReport not rendered successfully!')
    else:
        print(line_breaker.join(report_str), file=file)
        print(f"report saved to {report_file}") if file else None
    finally:
        file.close() if file else None

    return return_stats if return_stats else None
