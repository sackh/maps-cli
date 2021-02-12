"""Common utilities across project."""

from geojson import Feature, Point


def yield_subcommands(obj):
    """
    Show list of all available sub commands.

    :param obj: ``Click`` command object.
    """
    for name, value in obj.commands.items():
        if name != "show":
            yield name


def get_feature_from_lat_lon(lat: float, lon: float):
    """Returns GeoJSON Point Feature for a given latitude and longitude.

    :param lat: latitude of Point.
    :param lon: longitude of Point.
    :return: An object of :class:`goejson.Feature`
    """
    feature = Feature(geometry=Point((lon, lat)))
    return feature
