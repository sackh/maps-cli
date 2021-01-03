"""Main commands module. This module acts as entry point for all the commands."""
import click

import osm


@click.group()
def maps():
    """Map services of various providers."""


@maps.command()
def show():
    """show list of all maps services providers."""
    show_providers(maps)


def show_providers(obj):
    """
    Show list of all available maps services providers.

    :param obj: main maps click command group object.
    :return:
    """
    for name, value in obj.commands.items():
        if isinstance(value, click.Group):
            click.echo(name)


if __name__ == "__main__":
    maps.add_command(osm.osm)
    maps()
