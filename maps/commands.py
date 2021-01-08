"""Main commands module. This module acts as entry point for all the commands."""
import click

from maps.here import here
from maps.mapbox import mapbox
from maps.osm import osm
from maps.tomtom import tomtom
from maps.utils import yield_subcommands

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def maps():
    """Map services of various providers."""


@maps.command()
def show():
    """show list of all service providers."""
    for sub in yield_subcommands(maps):
        click.secho(sub, fg="green")


maps.add_command(osm)
maps.add_command(here)
maps.add_command(mapbox)
maps.add_command(tomtom)
