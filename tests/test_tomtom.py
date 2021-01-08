"""Module to test TomTom services."""
from click.testing import CliRunner

from maps.commands import maps


def test_geocoding_fwd():
    runner = CliRunner()
    result = runner.invoke(
        maps, ["tomtom", "geocoding", "--forward", "springfield"], catch_exceptions=False
    )
    assert result.exit_code == 0
    assert result.output == '{\n  "lat": 37.21552,\n  "lon": -93.29236\n}\n'


def test_geocoding_reverse():
    runner = CliRunner()
    result = runner.invoke(
        maps, ["tomtom", "geocoding", "--reverse", "19.16153,72.85618"], catch_exceptions=False
    )
    assert result.exit_code == 0
    assert "I B Patel Road" in result.output
