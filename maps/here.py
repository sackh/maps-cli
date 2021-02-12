"""This module defines all the HERE commands."""
import json
import os

import click
from geojsonio import display as geo_display
from geopy.geocoders import Here

from maps.exceptions import ApiKeyNotFoundError
from maps.utils import get_feature_from_lat_lon, yield_subcommands


@click.group()
@click.pass_context
def here(ctx):
    """Here provider."""
    ctx.obj = {}


@here.command()
def show():
    """show list of all sub commands."""
    for sub in yield_subcommands(here):
        click.secho(sub, fg="green")


@here.command(short_help="forward or reverse geocode for an address or coordinates.")
@click.argument("query", required=True)
@click.option("--apikey", help="Your HERE API key", type=str)
@click.option(
    "--forward/--reverse",
    default=True,
    show_default=True,
    help="Perform a forward or reverse geocode",
)
@click.option("--raw", is_flag=True)
@click.option("--display", help="Display result in browser", is_flag=True)
@click.pass_context
def geocoding(ctx, query, apikey, forward, raw, display):
    """
    HERE's geocoding service.
    \f

    :param ctx: A context dictionary.
    :param query: A string to represent address query for geocoding.
    :param apikey: An API key for authentication.
    :param forward: A boolean flag for forward/reverse geocoding.
    :param raw: A boolean flag to show api response as it is.
    :param display: A boolean flag to show result in web browser.
    :return: None.
    """
    apikey = apikey or os.environ.get("HERE_APIKEY")
    if apikey is None:
        raise ApiKeyNotFoundError(
            "Please pass HERE API KEY as --apikey or set it as environment "
            "variable in HERE_APIKEY "
        )
    ctx.obj["apikey"] = apikey
    geolocator = Here(apikey=ctx.obj["apikey"])
    if forward:
        location = geolocator.geocode(query)
        if raw:
            click.secho(json.dumps(location.raw, indent=2), fg="green")
        elif display:
            feature = get_feature_from_lat_lon(location.latitude, location.longitude)
            geo_display(feature)
        else:
            result = {"lat": location.latitude, "lon": location.longitude}
            click.secho(json.dumps(result, indent=2), fg="green")
    else:
        location = geolocator.reverse(query)
        if raw:
            click.secho(json.dumps(location.raw, indent=2), fg="green")
        else:
            click.secho(location.address, fg="green")
