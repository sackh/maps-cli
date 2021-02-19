"""Module to test utils."""

from maps.utils import get_feature_from_lat_lon


def test_get_feature_from_lat_lon():
    feature = get_feature_from_lat_lon(19, 73)
    assert feature == {
        "geometry": {"coordinates": [73, 19], "type": "Point"},
        "properties": {},
        "type": "Feature",
    }
