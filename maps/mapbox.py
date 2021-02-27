"""This module defines all the MapBox commands."""
import os

import click
import simplejson as json
from geojsonio import display as geo_display
from geopy.geocoders import MapBox

from maps.apis.mapbox import MapBoxApi
from maps.exceptions import ApiKeyNotFoundError
from maps.utils import get_feature_from_lat_lon, yield_subcommands


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
@click.option("--raw", help="Show response body as it is from API", is_flag=True)
@click.option("--display", help="Display result in browser", is_flag=True)
@click.pass_context
def geocoding(ctx, query, apikey, forward, raw, display):
    """
    MapBox's geocoding service.
    \f

    :param ctx: A context dictionary.
    :param query: A string to represent address query for geocoding.
    :param apikey: An API key for authentication.
    :param forward: A boolean flag for forward/reverse geocoding.
    :param raw: A boolean flag to show api response as it is.
    :param display: A boolean flag to show result in web browser.
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
@click.option("--display", help="Display result in browser", is_flag=True)
@click.pass_context
def isochrone(
    ctx, profile, coordinates, contours_minutes, contours_colors, polygons, apikey, display
):
    """
    An isochrone, from the Greek root words iso (equal) and chrone (time), is a line that connects
    points of equal travel time around a given location.

    The Mapbox Isochrone API computes areas that are reachable within a specified amount of time
    from a location, and returns the reachable regions as contours of polygons or lines that
    you can display on a map.
    \f

    :param ctx: A context dictionary.
    :param profile: A Mapbox Directions routing profile ID. Options are mapbox/driving for travel
        times by car, mapbox/walking for pedestrian and hiking travel times, and mapbox/cycling for
        travel times by bicycle. For more detailed descriptions of these routing profiles, see the
        Directions API documentation.
    :param coordinates: A {longitude,latitude} coordinate pair around which to center the isochrone
        lines.
    :param contours_minutes: The times in minutes to use for each isochrone contour. You can
        specify up to four contours. Times must be in increasing order. The maximum time that can
        be specified is 60 minutes.
    :param contours_colors: The colors to use for each isochrone contour, specified as hex values
        without a leading # (for example, ff0000 for red). If this parameter is used, there must
        be the same number of colors as there are entries in contours_minutes.
        If no colors are specified, the Isochrone API will assign a default rainbow color scheme
        to the output.
    :param polygons: Specify whether to return the contours as GeoJSON polygons (true) or
        linestrings (false, default). When polygons=true, any contour that forms a ring is
        returned as a polygon.
    :param apikey: An API key for authentication.
    :param display: A boolean flag to show result in web browser.
    :return: None.
    """
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
    if display:
        lon, lat = [float(c) for c in coordinates.split(",")]
        center = get_feature_from_lat_lon(lat, lon)
        feature_collection = resp.json()
        feature_collection["features"].append(center)
        geo_display(json.dumps(feature_collection, indent=2))
    else:
        click.secho(json.dumps(resp.json(), indent=2), fg="green")


@mapbox.command(short_help="The Mapbox Matrix API returns travel times between many points.")
@click.option(
    "--profile",
    type=click.Choice(["driving", "walking", "cycling", "driving-traffic"]),
    help="A Mapbox Directions routing profile ID.",
    required=True,
)
@click.option(
    "--coordinates",
    required=True,
    help="A semicolon separated {longitude,latitude} coordinate pairs.",
    type=str,
)
@click.option(
    "--annotations",
    help="Used to specify the resulting matrices. Possible values are: duration (default), "
    "distance, or both values separated by a comma.",
    default="duration",
)
@click.option(
    "--approaches",
    help="A semicolon-separated list indicating the side of the road from which to approach "
    "waypoints in a requested route. Accepts unrestricted (default, route can arrive at the "
    "waypoint from either side of the road) or curb (route will arrive at the waypoint on "
    "the driving_side of the region). If provided, the number of approaches must be the same "
    "as the number of waypoints. However, you can skip a coordinate and show its position in "
    "the list with the ; separator waypoints in a requested route",
)
@click.option(
    "--destinations",
    help="Use the coordinates at a given index as destinations. Possible values are: a "
    "semicolon-separated list of 0-based indices, or all (default). "
    "The option all allows using all coordinates as destinations.",
    type=str,
)
@click.option("--apikey", help="Your MapBox API key", type=str)
@click.pass_context
def matrix(ctx, profile, coordinates, annotations, approaches, destinations, apikey):
    """
    The Mapbox Matrix API returns travel times between many points.
    for more information `see <https://docs.mapbox.com/api/navigation/matrix/>_`.
    \f

    :param ctx: A context dictionary.
    :param profile: A Mapbox Directions routing profile ID.
        `see <https://docs.mapbox.com/api/navigation/matrix/>_`.
    :param coordinates: A semicolon-separated list of {longitude},{latitude} coordinates.
        There must be between two and 25 coordinates. For the mapbox/driving-traffic profile,
        the maximum is 10 coordinates.
    :param annotations: Used to specify the resulting matrices. Possible values are: duration
        (default), distance, or both values separated by a comma.
    :param approaches: A semicolon-separated list indicating the side of the road from which to
        approach waypoints in a requested route. Accepts unrestricted (default, route can arrive
        at the waypoint from either side of the road) or curb (route will arrive at the waypoint
        on the driving_side of the region). If provided, the number of approaches must be the same
        as the number of waypoints. However, you can skip a coordinate and show its position in the
        list with the ; separator.
    :param destinations: Use the coordinates at a given index as destinations. Possible values are:
        a semicolon-separated list of 0-based indices, or all (default). The option all allows
        using all coordinates as destinations.
    :param apikey: An API key for authentication.
    :return: None.
    """
    apikey = apikey or os.environ.get("MAPBOX_APIKEY")
    if apikey is None:
        raise ApiKeyNotFoundError(
            "Please pass MAPBOX API KEY as --apikey or set it as environment "
            "variable in MAPBOX_APIKEY "
        )
    ctx.obj["apikey"] = apikey
    client = MapBoxApi(base_url="https://api.mapbox.com", credentials=apikey)
    resp = client.matrix(
        profile=profile,
        coordinates=coordinates,
        annotations=annotations if annotations else None,
        approaches=approaches if approaches else None,
        destinations=destinations if destinations else None,
    )
    click.secho(json.dumps(resp.json(), indent=2), fg="green")
