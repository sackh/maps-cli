"""Module to test MapBox services."""
from click.testing import CliRunner

from maps.commands import maps


def test_geocoding_fwd():
    runner = CliRunner()
    result = runner.invoke(
        maps, ["mapbox", "geocoding", "--forward", "springfield"], catch_exceptions=False
    )
    assert result.exit_code == 0
    assert result.output == '{\n  "lat": 37.2153,\n  "lon": -93.2983\n}\n'


def test_geocoding_reverse():
    runner = CliRunner()
    result = runner.invoke(
        maps, ["mapbox", "geocoding", "--reverse", "19.16153,72.85618"], catch_exceptions=False
    )
    assert result.exit_code == 0
    assert "Haptik, 8th Floor" in result.output
