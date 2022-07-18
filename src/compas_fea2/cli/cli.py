"""
Console script for compas_fea2.
"""
import sys
import os
import click
from compas_fea2 import HOME

import os

import sys
from fea2_extension.main import init_plugin


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
@click.argument('backend')
def init_backend(backend, clean):
    """Initialize a bare backend module.\n
    backend : txt\n
        The name of the backend. This is must be lower case.
    """
    init_plugin(HOME, backend, clean)
    backend = backend.lower()


# -------------------------------- DEBUG ----------------------------------#
if __name__ == "__main__":
    sys.exit(main.init_backend())
