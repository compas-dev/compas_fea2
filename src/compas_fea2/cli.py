"""
Console script for compas_fea2.
"""

import importlib
import os
import sys

import click
import dotenv

from compas_fea2 import HOME
from compas_fea2 import VERBOSE

try:
    from fea2_extension.main import init_plugin  # type: ignore
except Exception:
    if VERBOSE:
        print("WARNING: fea2_extension module not installed.")


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
@click.option("--clean", default="False", help="remove existing directories")
@click.argument("backend")
def init_backend(backend, clean):
    """Initialize a bare backend module.\n
    backend : txt\n
        The name of the backend. This is must be lower case.
    """
    init_plugin(HOME, backend, clean)
    backend = backend.lower()


@main.command()
@click.argument("backend")
@click.argument("setting")
@click.argument("value")
def change_setting(backend, setting, value):
    """Change a setting for the specified backend.\n
        backend : txt\n
            The name of the backend.
        setting : txt\n
            The setting to be changed.
        value : txt\n
            The new value for the setting.

    Example usage:\n
        fea2 change-setting opensees exe "Applications/OpenSees3.5.0/bin/OpenSees"
    """
    m = importlib.import_module("compas_fea2_" + backend.lower())
    env = os.path.join(m.HOME, "src", "compas_fea2_" + backend.lower(), ".env")
    dotenv.set_key(env, setting.upper(), value)
    print(f"{setting.upper()} set to {value} for compas_fea2_{backend.lower()}")


# -------------------------------- DEBUG ----------------------------------#
if __name__ == "__main__":
    sys.exit(main.init_backend())
