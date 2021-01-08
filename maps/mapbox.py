"""This module defines all the MapBox commands."""
import json
import os

import click
from geopy.geocoders import MapBox

from maps.exceptions import ApiKeyNotFoundError
from maps.utils import yield_subcommands


@click.group()
@click.pass_context
def mapbox(ctx):
    """MapBox provider."""
    ctx.obj = {}


@mapbox.command()
def show():
    """show list of all sub commands."""
    for sub in yield_subcommands(mapbox):
        click.secho(sub, fg="green")


@mapbox.command(short_help="forward or reverse geocode for an address or coordinates.")
@click.argument("query", required=True)
@click.option("--apikey", help="Your MapBox API key", type=str)
@click.option(
    "--forward/--reverse",
    default=True,
    show_default=True,
    help="Perform a forward or reverse geocode",
)
@click.option("--raw", is_flag=True)
@click.pass_context
def geocoding(ctx, query, apikey, forward, raw):
    """MapBox's geocoding service."""
    apikey = apikey or os.environ.get("MAPBOX_APIKEY")
    if apikey is None:
        raise ApiKeyNotFoundError(
            "Please pass MAPBOX API KEY as --apikey or set it as environment "
            "variable in MAPBOX_APIKEY "
        )
    ctx.obj["apikey"] = apikey
    geolocator = MapBox(api_key=ctx.obj["apikey"])
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
