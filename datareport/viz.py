import pandas as pd
import matplotlib.pyplot as plt


def plot_time_series(df: pd.DataFrame, col_list: list, datetime: str = '') -> None:
    """

    :param df: input dataset
    :param datetime: target date variable, leave it empty if it is the index
    :param col_list: target columns
    :return:
    """
    n_col = len(col_list)
    if len(datetime) == 0:
        new_df = df
    else:
        col_list.append(datetime)
        new_df = df[col_list]
        new_df.set_index(datetime, inplace=True)

    new_df.index = pd.to_datetime(new_df.index)
    fig, axs = plt.subplots(n_col, 1, sharex=True)
    fig.subplots_adjust(hspace=0)
    for i in range(n_col):
        axs[i].scatter(new_df.index, new_df[col_list[i]], s=1)
        axs[i].set_ylabel(col_list[i])
