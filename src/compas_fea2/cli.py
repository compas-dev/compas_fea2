"""
Console script for compas_fea2.
"""
import sys
import os
import click
import json

from compas_fea2 import HOME
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
# @click.option('--clean', default='False', help='remove existing directories')
@click.argument("backend")
@click.argument("setting")
@click.argument("value")
def change_settings(backend, setting, value):
    """Change a setting for the specified backend.\n
    backend : txt\n
        The name of the backend.
    setting : txt\n
        The setting to be changed.
    value : txt\n
        The new value for the setting.
    """
    backend_settings = os.path.join(HOME, "src", "compas_fea2", "backends", backend.lower(), "settings.json")

    with open(backend_settings, "r") as f:
        settings = json.load(f)

    with open(backend_settings, "w") as f:
        settings[setting] = value
        json.dump(settings, f)


# -------------------------------- DEBUG ----------------------------------#
if __name__ == "__main__":
    sys.exit(main.init_backend())
