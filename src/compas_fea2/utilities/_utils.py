from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import itertools
import os
import subprocess
from functools import wraps
from time import perf_counter
from typing import Generator, Optional
import threading
import sys
import time

from compas_fea2 import VERBOSE


def with_spinner(message="Running"):
    """Decorator to add a spinner animation to a function."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            stop_event = threading.Event()
            spinner_thread = threading.Thread(target=spinner_animation, args=(message, stop_event))
            spinner_thread.start()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                stop_event.set()
                spinner_thread.join()

        return wrapper

    return decorator


def spinner_animation(message, stop_event):
    """Spinner animation for indicating progress."""
    spinner = "|/-\\"
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{message} {spinner[idx % len(spinner)]}")
        sys.stdout.flush()
        time.sleep(0.2)  # Adjust for speed
        idx += 1
    sys.stdout.write("\rDone!               \n")  # Clear the line when done


def timer(_func=None, *, message=None):
    """Print the runtime of the decorated function"""

    def decorator_timer(func):
        @wraps(func)
        def wrapper_timer(*args, **kwargs):
            start_time = perf_counter()  # 1
            value = func(*args, **kwargs)
            end_time = perf_counter()  # 2
            run_time = end_time - start_time  # 3
            if VERBOSE:
                m = message or "Finished {!r} in".format(func.__name__)
                print("{} {:.4f} secs".format(m, run_time))
            return value

        return wrapper_timer

    if _func is None:
        return decorator_timer
    else:
        return decorator_timer(_func)


def launch_process(cmd_args: list[str], cwd: Optional[str] = None, verbose: bool = False, **kwargs) -> Generator[bytes, None, None]:
    """Open a subprocess and yield its output line by line.

    Parameters
    ----------
    cmd_args : list[str]
        List of command arguments to execute.
    cwd : str, optional
        Path where to start the subprocess, by default None.
    verbose : bool, optional
        Print the output of the subprocess, by default `False`.

    Yields
    ------
    bytes
        Output lines from the subprocess.

    Raises
    ------
    FileNotFoundError
        If the command executable is not found.
    subprocess.CalledProcessError
        If the subprocess exits with a non-zero return code.
    """
    try:
        env = os.environ.copy()
        with subprocess.Popen(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd, shell=True, env=env, **kwargs) as process:
            assert process.stdout is not None
            for line in process.stdout:
                if verbose:
                    print(line.decode().strip())
                yield line

            process.wait()
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, cmd_args)

    except FileNotFoundError as e:
        print(f"Error: Command not found - {e}")
        raise
    except subprocess.CalledProcessError as e:
        print(f"Error: Command '{cmd_args}' failed with return code {e.returncode}")
        raise


class extend_docstring:
    def __init__(self, method, note=False):
        self.doc = method.__doc__

    def __call__(self, function):
        if self.doc is not None:
            doc = function.__doc__
            function.__doc__ = self.doc
            if doc is not None:
                function.__doc__ += doc
        return function


def get_docstring(cls):
    """
    Decorator: Append to a function's docstring.
    """

    def _decorator(func):
        func_name = func.__qualname__.split(".")[-1]
        doc_parts = getattr(cls, func_name).original.__doc__.split("Returns")
        note = """
        Returns
        -------
        list of {}

        """.format(
            doc_parts[1].split("-------\n")[1]
        )
        func.__doc__ = doc_parts[0] + note
        return func

    return _decorator


def part_method(f):
    """Run a part level method. In this way it is possible to bring to the
    model level some of the functions of the parts.

    Parameters
    ----------
    method : str
        name of the method to call.

    Returns
    -------
    [var]
        List results of the method per each part in the model.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        func_name = f.__qualname__.split(".")[-1]
        self_obj = args[0]
        res = [vars for part in self_obj.parts if (vars := getattr(part, func_name)(*args[1::], **kwargs))]
        if isinstance(res[0], list):
            res = list(itertools.chain.from_iterable(res))
        # res = list(itertools.chain.from_iterable(res))
        return res

    return wrapper


def step_method(f):
    """Run a step level method. In this way it is possible to bring to the
    problem level some of the functions of the steps.

    Parameters
    ----------
    method : str
        name of the method to call.

    Returns
    -------
    [var]
        List results of the method per each step in the problem.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        func_name = f.__qualname__.split(".")[-1]
        self_obj = args[0]
        res = [vars for step in self_obj.steps if (vars := getattr(step, func_name)(*args[1:], **kwargs))]
        res = list(itertools.chain.from_iterable(res))
        return res

    return wrapper


def problem_method(f):
    """Run a problem level method. In this way it is possible to bring to the
    model level some of the functions of the problems.

    Parameters
    ----------
    method : str
        name of the method to call.

    Returns
    -------
    [var]
        List results of the method per each problem in the model.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        func_name = f.__qualname__.split(".")[-1]
        self_obj = args[0]
        res = [vars for problem in self_obj.problems if (vars := getattr(problem, func_name)(*args[1::], **kwargs))]
        res = list(itertools.chain.from_iterable(res))
        return res

    return wrapper


def to_dimensionless(func):
    """Decorator to convert pint Quantity objects to dimensionless in the base units."""

    def wrapper(*args, **kwargs):
        new_args = [a.to_base_units().magnitude if hasattr(a, "to_base_units") else a for a in args]
        new_kwargs = {k: v.to_base_units().magnitude if hasattr(v, "to_base_units") else v for k, v in kwargs.items()}
        return func(*new_args, **new_kwargs)

    wrapper.original = func  # Preserve the original function
    return wrapper
