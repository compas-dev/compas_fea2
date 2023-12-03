from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import inspect
from subprocess import Popen
from subprocess import PIPE

from functools import wraps
from time import perf_counter

from compas.geometry import bounding_box
from compas.geometry import Point, Box
import importlib
import itertools
from typing import Iterable



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


def launch_process(cmd_args, cwd, verbose=False):
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
        if verbose:
            yield line

    # stdout, stderr = p.communicate()
    # return stdout.decode(), stderr.decode()


def _compute_model_dimensions(model):
    nodes = [Point(*node.xyz) for part in model.parts for node in part.nodes]
    bbox = bounding_box(nodes)
    box = Box.from_bounding_box(bbox)
    return box.width, box.height, box.depth


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
        func_name = func.__qualname__.split('.')[-1]
        doc_parts = getattr(cls, func_name).__doc__.split('Returns')
        note = """
        Returns
        -------
        list of {}

        """.format(doc_parts[1].split('-------\n')[1])
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
    {:class:`compas_fea2.model.DeformablePart`: var}
        dictionary with the results of the method per each part in the model.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        func_name = f.__qualname__.split('.')[-1]
        self_obj = args[0]
        if kwargs.get('dict_format', None):
            return {part: vars for part in self_obj.parts if (vars := getattr(part, func_name)(*args[1::], **kwargs))}
        else:
            res = [vars for part in self_obj.parts if (vars := getattr(part, func_name)(*args[1::], **kwargs))]
            if kwargs.get('merge', None):
                list(itertools.chain.from_iterable(res))
            return res
    # func_name = f.__qualname__.split('.')[-1]
    # wrapper.__doc__ = getattr(DeformablePart, func_name).__doc__.split('Returns')[0]
    # wrapper.__doc__ += "ciao"

#         docs = getattr(DeformablePart, method).__doc__.split('Returns', 1)[0]
#         docs += """
# Returns
# -------
# {:class:`compas_fea2.model.DeformablePart`: var}
#     dictionary with the results of the method per each part in the model.
# """

    return wrapper


# TODO combine with part_method
def step_method(f):
    """Run a step level method. In this way it is possible to bring to the
    problem level some of the functions of the steps.

    Parameters
    ----------
    method : str
        name of the method to call.

    Returns
    -------
    {:class:`compas_fea2.problem._Step`: var}
        dictionary with the results of the method per each step in the problem.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        func_name = f.__qualname__.split('.')[-1]
        self_obj = args[0]
        return {step: vars for step in self_obj.steps if (vars := getattr(step, func_name)(*args[1::], **kwargs))}
    return wrapper


# TODO combine with part_method
# TODO add parameter to differentiate from action and return dict or add @problem_step_method
def problem_method(f):
    """Run a problem level method. In this way it is possible to bring to the
    model level some of the functions of the problems.

    Parameters
    ----------
    method : str
        name of the method to call.

    Returns
    -------
    {:class:`compas_fea2.problem.Problem`: var}
        dictionary with the results of the method per each step in the problem.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        func_name = f.__qualname__.split('.')[-1]
        self_obj = args[0]
        problems = kwargs.setdefault('problems', self_obj.problems)
        if not problems:
            raise ValueError('No problems found in the model')
        if not isinstance(problems, Iterable):
            problems = [problems]
        vars = {}
        for problem in problems:
            if problem.model != self_obj:
                raise ValueError('{} is not registered to this model'.format(problem))
            if 'steps' in kwargs:
                kwargs.setdefault('steps', self_obj.steps)
            var = getattr(problem, func_name)(*args[1::], **kwargs)
            if var:
                vars[problem] = vars
        return vars
    return wrapper
