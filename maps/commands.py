"""Main commands module. This module acts as entry point for all the commands."""
import click

from maps.osm import osm


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
    """
    for name, value in obj.commands.items():
        if isinstance(value, click.Group):
            click.secho(name, fg="green")


maps.add_command(osm)

