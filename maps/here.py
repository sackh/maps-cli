"""This module defines all the HERE commands."""
import json
import os

import click
from geopy.geocoders import Here

from maps.utils import yield_subcommands


@click.group()
@click.option("--apikey", help="Your HERE API key")
@click.pass_context
def here(ctx, apikey):
    """Here provider."""
    ctx.obj = {}
    apikey = apikey or os.environ.get("HERE_APIKEY")
    ctx.obj["apikey"] = apikey


@here.command()
def show():
    """show list of all sub commands."""
    for sub in yield_subcommands(here):
        click.secho(sub, fg="green")


@here.command(short_help="forward or reverse geocode for an address or coordinates.")
@click.argument("query", required=True)
@click.option(
    "--forward/--reverse",
    default=True,
    help="Perform a forward or reverse geocode. [default: forward]",
)
@click.option("--raw", is_flag=True)
@click.pass_context
def geocoding(ctx, query, forward, raw):
    """HERE's geocoding service."""
    geolocator = Here(apikey=ctx.obj["apikey"])
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
