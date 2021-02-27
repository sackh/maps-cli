"""This module defines all the HERE commands."""
import os

import click
import simplejson as json
from geojsonio import display as geo_display
from geopy.geocoders import Here
from here_location_services import LS

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


@here.command(short_help="Search places using free-form text query.")
@click.argument("query", required=True)
@click.option(
    "--coordinates",
    help="A {longitude,latitude} coordinate pair around which search query will be applied.",
    type=str,
)
@click.option(
    "--radius", help="radius in meters along with coordinates for searching places.", type=str
)
@click.option(
    "--country_codes", help="comma separated ISO 3166-1 alpha-3 country codes.", type=str
)
@click.option(
    "--bounding_box",
    help="A bounding box, provided as {west longitude},{south latitude},{east longitude},"
    "{north latitude}",
    type=str,
)
@click.option("--limit", help="Maximum numbers of results to be returned.", type=str)
@click.option(
    "--lang",
    help="language to be used for result rendering from a list of BCP47 compliant Language Codes.",
    type=str,
)
@click.option("--apikey", help="Your HERE API key", type=str)
@click.option("--raw", is_flag=True)
@click.option("--display", help="Display result in browser", is_flag=True)
@click.pass_context
def discover(
    ctx, query, coordinates, radius, country_codes, bounding_box, limit, lang, apikey, raw, display
):
    """
    Search places using free-form text query.
    There are multiple combination of inputs for restricting your search

    - ``center`` and ``country_code``
    - ``center`` and ``radius``
    - ``bounding_box``

    \f

    :param ctx:
    :param query:
    :param coordinates:
    :param radius:
    :param country_codes:
    :param bounding_box:
    :param limit:
    :param lang:
    :param apikey:
    :param raw:
    :param display:
    :return:
    """
    apikey = apikey or os.environ.get("HERE_APIKEY")
    if apikey is None:
        raise ApiKeyNotFoundError(
            "Please pass HERE API KEY as --apikey or set it as environment "
            "variable in HERE_APIKEY "
        )
    ctx.obj["apikey"] = apikey
    ls = LS(api_key=apikey)
    result = ls.discover(
        query=query,
        center=coordinates.split(",")[::-1] if coordinates else coordinates,
        radius=radius,
        country_codes=country_codes.split(",") if country_codes else country_codes,
        bounding_box=bounding_box.split(",") if bounding_box else bounding_box,
        limit=limit,
        lang=lang,
    )
    if raw:
        click.secho(json.dumps(result.response, indent=2), fg="green")
    elif display:
        geo_display(json.dumps(result.to_geojson(), indent=2))
    else:
        click.secho(json.dumps(result.items, indent=2), fg="green")
