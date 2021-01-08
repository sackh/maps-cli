"""Module to test OSM services."""
import json

from click.testing import CliRunner

from maps.commands import maps


def test_show():
    """Test osm show command."""
    runner = CliRunner()
    result = runner.invoke(maps, ["osm", "show"], catch_exceptions=False)
    assert result.output == "geocoding\n"


def test_geocoding_fwd():
    runner = CliRunner()
    result = runner.invoke(
        maps, ["osm", "geocoding", "--forward", "1600 pennsylvania ave nw"], catch_exceptions=False
    )
    assert result.exit_code == 0
    latlon = json.loads(result.output)
    lat, lon = latlon["lat"], latlon["lon"]
    lat = round(lat, 1)
    lon = round(lon, 2)
    assert lat == 39.7 and lon == -77.72


def test_geocoding_reverse():
    runner = CliRunner()
    result = runner.invoke(
        maps, ["osm", "geocoding", "--reverse", "19.16153,72.85618"], catch_exceptions=False
    )
    assert result.exit_code == 0
    assert "I B Patel Road" in result.output
