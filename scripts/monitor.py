import time
import tracemalloc
from functools import wraps


def monitor_time_memory(original_func):

    @wraps(original_func)
    def wrapped_func(*args, **kwargs):
        time_start = time.time()
        tracemalloc.start()

        func = original_func(*args, **kwargs)

        current, peak = tracemalloc.get_traced_memory()
        time_end = time.time() - time_start
        print(
            f"{original_func.__name__} finished in {time_end:.2f} sec, Current memory usage is {current / 10 ** 6}MB; "
            f"Peak memory usage was {peak / 10 ** 6}MB")
        tracemalloc.stop()
        return func

    return wrapped_func
