

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from subprocess import Popen
from subprocess import PIPE

from functools import wraps
from time import perf_counter

from compas.geometry import bounding_box
from compas.geometry import Point, Box


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


def launch_process(cmd_args, cwd, output=False):
    """Open a subprocess and print the output.

    Parameters
    ----------
    cmd_args : list[str]
        problem object.
    cwd : str
        path where to start the subprocess
    output : bool, optional
        print the output of the subprocess, by default `False`.

    Returns
    -------
    None

    """
    p = Popen(cmd_args, stdout=PIPE, stderr=PIPE, cwd=cwd, shell=True, env=os.environ)
    while True:
        line = p.stdout.readline()
        if not line:
            break
        line = line.strip().decode()
        if output:
            yield line

    # stdout, stderr = p.communicate()
    # return stdout.decode(), stderr.decode()


def _compute_model_dimensions(model):
    nodes = [Point(*node.xyz) for part in model.parts for node in part.nodes]
    bbox = bounding_box(nodes)
    box = Box.from_bounding_box(bbox)
    return box.width, box.height, box.depth
