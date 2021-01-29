"""This module defines all the OSM commands."""
import json

import click
import overpy
import pandas as pd
from geopy.geocoders import Nominatim
from tabulate import tabulate

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


@osm.command(short_help="OSM's Overpass API")
@click.argument("query", required=True)
def overpass(query):
    """OSM's Overpass API service."""
    api = overpy.Overpass()
    result = api.query(query)
    node_tags = []
    for node in result.nodes:
        node.tags["latitude"] = node.lat
        node.tags["longitude"] = node.lon
        node.tags["id"] = node.id
        node_tags.append(node.tags)
    nodes_df = pd.DataFrame(node_tags)
    if not nodes_df.empty:
        click.secho("Nodes:", fg="green")
        click.secho((tabulate(nodes_df, headers="keys", tablefmt="psql")), fg="green")
    ways = []
    for way in result.ways:
        way.tags["id"] = way.id
        ways.append(way.tags)
    ways_df = pd.DataFrame(ways)
    if not ways_df.empty:
        click.secho("Ways:", fg="green")
        click.secho((tabulate(ways_df, headers="keys", tablefmt="psql")), fg="green")
    relations = []
    for relation in result.relations:
        relation.tags["id"] = relation.id
        relations.append(relation.tags)
    relations_df = pd.DataFrame(relations)
    if not relations_df.empty:
        click.secho("Relations:", fg="green")
        click.secho((tabulate(relations_df, headers="keys", tablefmt="psql")), fg="green")
