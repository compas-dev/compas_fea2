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

    base_path = os.path.join(HOME, 'src', 'compas_fea2', 'backends')
    path = os.path.join(base_path, backend)
    if clean and os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

    # Build the __init__ file from the abaqus one
    # TODO change with automated jinja template
    base_path = os.path.join(HOME, 'src', 'compas_fea2', 'backends', 'abaqus', '__init__.py')
    with open(base_path, 'r') as file:
        filedata = file.read()
    # Replace the target string
    filedata = filedata.replace('abaqus', backend)
    filedata = filedata.replace('Abaqus', backend.capitalize())
    filedata = filedata.replace('ABAQUS', backend.upper())

    # Write the file out again
    with open(os.path.join(path, '__init__.py'), 'w') as file:
        file.write(filedata)
    for module_name in ['model', 'problem', 'optimisation', 'results', 'job']:
        module_path = os.path.join(path, module_name)
        if not os.path.exists(module_path):
            os.mkdir(module_path)
        module = importlib.import_module(".".join(['compas_fea2', module_name]))
        classes_data = scan_package(module, ignore_protected=True)

        mirror_package(path=module_path, package_data=classes_data, backend=backend)


# -------------------------------- DEBUG ----------------------------------#
if __name__ == "__main__":
    sys.exit(main.init_backend())
