"""
Console script for compas_fea2.
"""
import sys
import os
from pathlib import Path
import click
import compas_fea2


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

    click.echo("\nHey there! this is the command line interface (CLI) for compas_fea2!\n")


# -------------------------------- DEBUG ----------------------------------#
if __name__ == "__main__":
    sys.exit(main())
