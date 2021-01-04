"""Main commands module. This module acts as entry point for all the commands."""
import click

from maps.osm import osm
from maps.here import here
from maps.utils import yield_subcommands


@click.group()
def maps():
    """Map services of various providers."""


@maps.command()
def show():
    """show list of all sub commands of maps."""
    for sub in yield_subcommands(maps):
        click.secho(sub, fg="green")


maps.add_command(osm)
maps.add_command(here)

# if __name__ == "__main__":
#     maps()
