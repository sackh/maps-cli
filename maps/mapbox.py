"""This module defines all the MapBox commands."""
import json
import os

import click
from geopy.geocoders import MapBox

from maps.apis.mapbox import MapBoxApi
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
    """
    MapBox's geocoding service.
    \f

    :param ctx: A context dictionary.
    :param query: A string to represent address query for geocoding.
    :param apikey: An API key for authentication.
    :param forward: A boolean flag for forward/reverse geocoding.
    :param raw: A boolean flag to show api response as it is.
    :return: None.
    """
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


@mapbox.command(short_help="isochrone to get reachable areas on map.")
@click.option("--profile", type=click.Choice(["driving", "walking", "cycling"]), required=True)
@click.option(
    "--coordinates",
    required=True,
    help="A {longitude,latitude} coordinate pair around which to center the isochrone lines.",
    type=str,
)
@click.option(
    "--contours_minutes",
    required=True,
    help="The times in minutes to use for each isochrone contour",
    type=str,
)
@click.option(
    "--contours_colors",
    help="The colors to use for each isochrone contour, specified as hex values without a leading "
    "# (for example, ff0000 for red).",
    type=str,
)
@click.option(
    "--polygons",
    is_flag=True,
    help="Specify whether to return the contours as GeoJSON polygons (True) or linestrings "
    "(False).",
)
@click.option("--apikey", help="Your MapBox API key", type=str)
@click.pass_context
def isochrone(ctx, profile, coordinates, contours_minutes, contours_colors, polygons, apikey):
    """
    An isochrone, from the Greek root words iso (equal) and chrone (time), is a line that connects
    points of equal travel time around a given location.

    The Mapbox Isochrone API computes areas that are reachable within a specified amount of time
    from a location, and returns the reachable regions as contours of polygons or lines that
    you can display on a map.
    \f

    :param ctx: A context dictionary.
    :param profile:
    :param coordinates:
    :param contours_minutes:
    :param contours_colors:
    :param polygons:
    :param apikey:
    :return:
    """
    print("IN")
    apikey = apikey or os.environ.get("MAPBOX_APIKEY")
    if apikey is None:
        raise ApiKeyNotFoundError(
            "Please pass MAPBOX API KEY as --apikey or set it as environment "
            "variable in MAPBOX_APIKEY "
        )
    ctx.obj["apikey"] = apikey
    client = MapBoxApi(base_url="https://api.mapbox.com", credentials=apikey)
    resp = client.isochrone(
        profile=profile,
        coordinates=coordinates.split(","),
        contours_minutes=contours_minutes.split(","),
        contours_colors=contours_colors.split(",") if contours_colors else contours_colors,
        polygons=polygons,
    )
    click.secho(json.dumps(resp.json(), indent=2), fg="green")
