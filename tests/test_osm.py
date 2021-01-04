"""Module to test OSM services."""
from click.testing import CliRunner

from maps.commands import maps


def test_geocoding_fwd():
    runner = CliRunner()
    result = runner.invoke(
        maps, ["osm", "geocoding", "--forward", "1600 pennsylvania ave nw"], catch_exceptions=False
    )
    assert result.exit_code == 0
    assert result.output == '{\n  "lat": 39.7260958,\n  "lon": -77.7244815\n}\n'


def test_geocoding_reverse():
    runner = CliRunner()
    result = runner.invoke(
        maps, ["osm", "geocoding", "--reverse", "19.16153,72.85618"], catch_exceptions=False
    )
    assert result.exit_code == 0
    assert "I B Patel Road" in result.output
