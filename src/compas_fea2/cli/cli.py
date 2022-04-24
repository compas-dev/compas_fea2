"""
Console script for compas_fea2.
"""
import sys
import os
import shutil
import click
import compas_fea2
from compas_fea2 import HOME, DATA

import importlib
import compas_fea2.model
import inspect
from inspect import getmembers, isfunction, ismodule, isclass

import os
from jinja2 import Environment, FileSystemLoader

from compas_fea2.utilities._cookiecutter import scan_package, mirror_package


# -------------------------------- MAIN ----------------------------------#
@click.group()
def main():
    """fea2 main.

    Run `fea2 ono-o-one` for more info.
    """
    pass


@main.command()
def one_o_one():
    """Basic explanation of command line usage."""

    click.echo("\nHey there! this is the command line interface (CLI) for compas_fea2!\nWIP")


@main.command()
@click.option('--clean', default='False', help='remove existing directories')
@click.argument('backend', default='abaqus')
def init_backend(backend, clean):
    """Initialize a bare backend module.\n
    backend : txt\n
        The name of the backend. This is must be lower case.
    """
    backend = backend.lower()
    classes_data = scan_package(compas_fea2.problem, ignore_protected=True)
    base_path = os.path.join(HOME, 'src', 'compas_fea2', 'backends')
    path = os.path.join(base_path, backend)
    if clean and os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

    mirror_package(path=path, package_data=classes_data, backend='backend')


# -------------------------------- DEBUG ----------------------------------#
if __name__ == "__main__":
    sys.exit(main())
