"""Module to test HERE services."""
import json

from click.testing import CliRunner

from maps.commands import maps


def test_show():
    """Test here show command."""
    runner = CliRunner()
    result = runner.invoke(maps, ["here", "show"], catch_exceptions=False)
    assert result.output == "geocoding\n"


def test_geocoding_fwd():
    runner = CliRunner()
    result = runner.invoke(
        maps, ["here", "geocoding", "--forward", "springfield"], catch_exceptions=False
    )
    assert result.exit_code == 0
    assert result.output == '{\n  "lat": 37.20897,\n  "lon": -93.29159\n}\n'
    result = runner.invoke(
        maps, ["here", "geocoding", "--forward", "springfield", "--raw"], catch_exceptions=False
    )
    res = json.loads(result.output)
    assert res["Location"]["LocationType"] == "point"


def test_geocoding_reverse():
    runner = CliRunner()
    result = runner.invoke(
        maps, ["here", "geocoding", "--reverse", "19.16153,72.85618"], catch_exceptions=False
    )
    assert result.exit_code == 0
    assert "I B Patel Road" in result.output
