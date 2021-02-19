"""Module to test OSM services."""
import json

from click.testing import CliRunner

from maps.commands import maps


def test_show():
    """Test osm show command."""
    runner = CliRunner()
    result = runner.invoke(maps, ["osm", "show"], catch_exceptions=False)
    assert result.output == "geocoding\noverpass\n"


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

    raw_result = runner.invoke(
        maps,
        ["osm", "geocoding", "--forward", "1600 pennsylvania ave nw", "--raw"],
        catch_exceptions=False,
    )
    assert raw_result.exit_code == 0
    assert "place_id" in raw_result.output


def test_geocoding_reverse():
    runner = CliRunner()
    result = runner.invoke(
        maps, ["osm", "geocoding", "--reverse", "19.16153,72.85618"], catch_exceptions=False
    )
    assert result.exit_code == 0
    assert "I B Patel Road" in result.output
    raw_result = runner.invoke(
        maps,
        ["osm", "geocoding", "--reverse", "19.16153,72.85618", "--raw"],
        catch_exceptions=False,
    )
    assert raw_result.exit_code == 0


def test_overpass_node():
    runner = CliRunner()
    result = runner.invoke(
        maps, ["osm", "overpass", "node(50.745,7.17,50.75,7.18);out;"], catch_exceptions=False
    )
    assert result.exit_code == 0
    assert '"id": 4597400934' in result.output


def test_overpass_way():
    runner = CliRunner()
    result = runner.invoke(
        maps, ["osm", "overpass", "way(50.745,7.17,50.75,7.18);out;"], catch_exceptions=False
    )
    assert result.exit_code == 0
    assert '"addr:city": "Bonn"' in result.output


def test_overpass_relation():
    runner = CliRunner()
    result = runner.invoke(
        maps, ["osm", "overpass", "relation(50.745,7.17,50.75,7.18);out;"], catch_exceptions=False
    )
    assert result.exit_code == 0
    assert '"landuse": "forest"' in result.output
