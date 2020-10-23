"""A module for monitoring profiling performance."""

import time
import tracemalloc
from functools import wraps

from colorama import Fore
from loguru import logger


def monitor_time_memory(original_func):
    """Monitor command computational consumptions.

    :param original_func:
    :return:
    """

    @wraps(original_func)
    def wrapped_func(*args, **kwargs):
        time_start = time.time()
        tracemalloc.start()
        func = original_func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        time_end = time.time() - time_start
        tracemalloc.stop()
        print(Fore.BLUE +
              f"{original_func.__name__} finished in {time_end:.2f} sec, "
              f"Current memory usage is {current / 10 ** 6:.2f}MB; "
              f"Peak memory usage was {peak / 10 ** 6:.2f}MB" + Fore.RESET)
        logger.debug(f"Time: {time_end:.2f} sec, Ending memory: {current / 10 ** 6:.2f}MB, "
                     f"Peak memory: {current / 10 ** 6:.2f}MB")
        return func

    return wrapped_func
