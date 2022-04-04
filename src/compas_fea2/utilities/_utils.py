from functools import wraps
from time import perf_counter


def timer(_func=None, *, message=None):
    """Print the runtime of the decorated function"""
    def decorator_timer(func):
        @wraps(func)
        def wrapper_timer(*args, **kwargs):
            start_time = perf_counter()    # 1
            value = func(*args, **kwargs)
            end_time = perf_counter()      # 2
            run_time = end_time - start_time    # 3
            m = message or 'Finished {!r} in'.format(func.__name__)
            print('{} {:.4f} secs'.format(m, run_time))
            return value
        return wrapper_timer

    if _func is None:
        return decorator_timer
    else:
        return decorator_timer(_func)
