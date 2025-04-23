"""Print or save a report of overall statistics and detailed statistics for a given dataset."""

import sys
from datetime import date
from pathlib import Path
from typing import Optional, Union, Dict, Tuple, List
import warnings

import pandas as pd
from colorama import Fore, init
from loguru import logger
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.exceptions import NotFittedError

from ._monitor import monitor_time_memory
from ._config import DEFAULT_SAMPLE_SIZE, RANDOM_STATE
from ._profiling import get_df_profile, get_a_sample

# Custom warning for changed behavior
class ChangedBehaviorWarning(UserWarning):
    """Warning for changed behavior after fitting."""
    pass

init(autoreset=True)
logger.remove()
logger.add(sys.stdout, format="{time:YYYY-MM-DD at HH:mm:ss}|{level}|{message}", level="WARNING")


def _str_format(f_name: str) -> Tuple[str, str]:
    """Return correct table and line breaker format base on the name of the file to store output.

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
                   var_per_row: int = 6, table_fmt: str = 'psql', line_breaker: str = '\n') -> List[str]:
    """
    Convert all statistics to a list of strings.

    :param df_profile: a dictionary of statistics
    :param var_per_row: number of columns to show on each row
    :param table_fmt: the string format of dataframe
    :param line_breaker:
    :return: a list of strings
    """
    logger.info("Convert statistics into strings...")
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
    for key, item in df_profile['var_stats'].items():
        report_str.append(f'{line_breaker}{key} variables:')
        for i in range(len(df_profile['var_stats'][f'{key}']) // (var_per_row + 1) + 1):
            dt = pd.DataFrame(item).T.iloc[:, i * var_per_row:(i + 1) * var_per_row]
            report_str.append(tabulate(
                dt, headers='keys', tablefmt=table_fmt) if table_fmt != 'html' else dt.to_html())
    report_str.append(f'{line_breaker}')

    if 'conf_matrix' in df_profile:
        report_str.append(' Confusion Matrix '.center(padding_size2, '='))
        for confusion_matrix in df_profile['conf_matrix']:
            report_str.append(f"row:{confusion_matrix.index.name} - col:{confusion_matrix.columns.name}")
            report_str.append(tabulate(confusion_matrix, headers=confusion_matrix.columns,
                                       showindex=confusion_matrix.index.to_list(),
                                       tablefmt=table_fmt) if table_fmt != 'html' else confusion_matrix.to_html())
    report_str.append(' End of report '.center(padding_size, '='))
    report_str.append(' Author of Dataprofile: Gordon Chen (GordonChen.GoBlue@gmail.com) '.center(padding_size, '='))
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
                 num_works: int = -1) -> None:
    """Print to screen or save a profile report to a file for a given pandas dataframe."""
    if sample_size > 0:
        sample_df = get_a_sample(df, sample_size, random_state)
    else:
        sample_df = df

    df_profile = get_df_profile(sample_df, num_works)
    if report_file:
        save_report(df_profile, var_per_row, report_file)
    else:
        print_report(df_profile, var_per_row)


class ProfileReport(BaseEstimator, TransformerMixin):
    """Print to screen or save a profile report to a given pandas dataframe."""

    def __init__(self,
                 sample_size: int = DEFAULT_SAMPLE_SIZE,
                 var_per_row: int = 6,
                 random_state: int = RANDOM_STATE,
                 num_works: int = -1) -> None:
        """Initialize class."""
        self._sample_size = sample_size
        self._var_per_row = var_per_row
        self._random_state = random_state
        self._num_works = num_works
        self.df_profile: Optional[Dict] = None
        self._is_new_arg = False

    @property
    def sample_size(self) -> int:
        return self._sample_size

    @sample_size.setter
    def sample_size(self, new_sample_size) -> None:
        self._sample_size = new_sample_size
        self._is_new_arg = True
        print(f"sample size set to {self._sample_size}")

    @property
    def var_per_row(self) -> int:
        return self._var_per_row

    @var_per_row.setter
    def var_per_row(self, new_var_per_row) -> None:
        self._var_per_row = new_var_per_row
        self._is_new_arg = True
        print(f"sample size set to {self._var_per_row}")

    @property
    def num_works(self) -> int:
        return self._num_works

    @num_works.setter
    def num_works(self, new_num_works) -> None:
        self._num_works = new_num_works
        self._is_new_arg = True
        print(f"sample size set to {self._num_works}")

    @property
    def random_state(self) -> int:
        return self._random_state

    @random_state.setter
    def random_state(self, new_random_state) -> None:
        self._random_state = new_random_state
        self._is_new_arg = True
        print(f"sample size set to {self._random_state}")

    def _check_fitted(self) -> None:
        """
        Check if the data profile file has been rendered.

        :return:
        """
        if not self.df_profile:
            raise NotFittedError

    def _check_new_args(self) -> None:
        """
        Check if the arguments have been updated since last fit.

        :return:
        """
        if self._is_new_arg:
            raise ChangedBehaviorWarning("new args inputted after last fit!")

    def fit(self, X: pd.DataFrame, y=None):
        """Fit the profiler to the data."""
        self._df_to_profile(X)
        self._is_new_arg = False
        return self

    def transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        """Transform the data (shows report and returns original data)."""
        self.show_report()
        return X

    def _df_to_profile(self, df: pd.DataFrame) -> None:
        """
        Get the data profile.

        :param df:
        :return:
        """
        if self._sample_size > 0:
            sample_df = get_a_sample(df, self._sample_size, self._random_state)
        else:
            sample_df = df

        self.df_profile = get_df_profile(sample_df, self._num_works)

    def show_report(self) -> None:
        """
        Print the data profile to the screen.

        :return:
        """
        self._check_fitted()
        self._check_new_args()
        print_report(self.df_profile, self._var_per_row)

    def save_report(self, report_file: str) -> None:
        """
        Save the data profile to as file.

        :param report_file:
        :return:
        """
        if report_file.split('.')[-1] not in ['md', 'html', 'txt']:
            raise NotImplementedError("file type doesn't support!")
        self._check_fitted()
        self._check_new_args()
        save_report(self.df_profile, self._var_per_row, report_file)
        print(f"Report saved to {report_file}")

    def __str__(self):
        table_fmt = 'psql'
        line_breaker = '\n'
        report_str = profile_to_str(self.df_profile, self._var_per_row, table_fmt, line_breaker)
        return line_breaker.join(report_str)
