"""This module defines all the ORS(https://openrouteservice.org/services/) commands."""
import os

import click
import openrouteservice as opnrs
import simplejson as json
from geojsonio import display as geo_display

from maps.exceptions import ApiKeyNotFoundError
from maps.utils import yield_subcommands


@click.group()
@click.pass_context
def ors(ctx):
    """ORS (https://openrouteservice.org/) provider."""
    ctx.obj = {}


@ors.command()
def show():
    """show list of all sub commands."""
    for sub in yield_subcommands(ors):
        click.secho(sub, fg="green")


@ors.command(short_help="forward or reverse geocode for an address or coordinates.")
@click.argument("query", required=True)
@click.option("--apikey", help="Your ORS API key", type=str)
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
    Open Route Service geocoding service.
    \f

    :param ctx: A context dictionary.
    :param query: A string to represent address query for geocoding.
    :param apikey: An API key for authentication.
    :param forward: A boolean flag for forward/reverse geocoding.
    :param raw: A boolean flag to show api response as it is.
    :param display: A boolean flag to show result in web browser.
    :return: None.
    """
    apikey = apikey or os.environ.get("ORS_APIKEY")
    if apikey is None:
        raise ApiKeyNotFoundError(
            "Please pass Open Route Service API KEY as --apikey or set it as environment "
            "variable in ORS_APIKEY "
        )
    ctx.obj["apikey"] = apikey
    geolocator = opnrs.Client(key=ctx.obj["apikey"])
    if forward:
        geocode = geolocator.pelias_search(text=query)
        if raw:
            click.secho(json.dumps(geocode, indent=2), fg="green")
        elif display:
            geocode.pop("geocoding")
            geo_display(json.dumps(geocode))
        else:
            for feature in geocode["features"]:
                coords = feature["geometry"]["coordinates"]
                result = {"lat": coords[1], "lon": coords[0]}
                click.secho(json.dumps(result, indent=2), fg="green")
    else:
        coordinate = query.split(",")
        reverse = geolocator.pelias_reverse(point=coordinate, validate=False)
        if raw:
            for result in reverse["features"]:
                click.secho(json.dumps(result, indent=2), fg="green")
        else:
            for result in reverse["features"]:
                click.secho(result["properties"]["label"], fg="green")
