"""Module to test ORS services."""
import json
import os

from click.testing import CliRunner

from maps.commands import maps


def test_show():
    """Test ors show command."""
    runner = CliRunner()
    result = runner.invoke(maps, ["ors", "show"], catch_exceptions=False)
    assert result.output.split() == ["geocoding"]


def test_geocoding_fwd():
    runner = CliRunner()
    result = runner.invoke(
        maps, ["ors", "geocoding", "--forward", "springfield"], catch_exceptions=False
    )
    assert result.exit_code == 0
    result = runner.invoke(
        maps, ["ors", "geocoding", "--forward", "springfield", "--raw"], catch_exceptions=False
    )
    res = json.loads(result.output)
    with open("ors_data", "w") as fh:
        json.dump(res, fh)
    assert res["type"] == "FeatureCollection"


def test_geocoding_exception():
    api_key = os.environ["ORS_APIKEY"]
    try:
        del os.environ["ORS_APIKEY"]
        runner = CliRunner()
        result = runner.invoke(
            maps, ["ors", "geocoding", "--forward", "springfield"], catch_exceptions=False
        )
    finally:
        os.environ["ORS_APIKEY"] = api_key
    assert result.exit_code == 2


def test_mock_display(mocker):
    mocker.patch("maps.ors.geo_display", return_value=True)
    runner = CliRunner()
    result = runner.invoke(
        maps,
        ["ors", "geocoding", "--forward", "springfield", "--display"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
