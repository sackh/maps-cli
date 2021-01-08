"""This module defines all the OSM commands."""
import json

import click
from geopy.geocoders import Nominatim

from maps import __version__
from maps.utils import yield_subcommands


@click.group()
def osm():
    """Open Street Map provider."""


@osm.command()
def show():
    """show list of all sub commands."""
    for sub in yield_subcommands(osm):
        click.secho(sub, fg="green")


@osm.command(short_help="forward or reverse geocode for an address or coordinates.")
@click.argument("query", required=True)
@click.option(
    "--forward/--reverse",
    default=True,
    show_default=True,
    help="Perform a forward or reverse geocode",
)
@click.option("--raw", is_flag=True)
def geocoding(query, forward, raw):
    """OSM's Nominatim geocoding service."""
    geolocator = Nominatim(user_agent=f"maps-cli/{__version__}")
    if forward:
        location = geolocator.geocode(query)
        if raw:
            click.secho(json.dumps(location.raw, indent=2), fg="green")
        else:
            result = {"lat": location.latitude, "lon": location.longitude}
            click.secho(json.dumps(result, indent=2), fg="green")
    else:
        location = geolocator.reverse(query)
        if raw:
            click.secho(json.dumps(location.raw, indent=2), fg="green")
        else:
            click.secho(location.address, fg="green")
