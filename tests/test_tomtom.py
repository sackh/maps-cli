"""Module to test TomTom services."""
import os

from click.testing import CliRunner

from maps.commands import maps


def test_show():
    """Test tomtom show command."""
    runner = CliRunner()
    result = runner.invoke(maps, ["tomtom", "show"], catch_exceptions=False)
    assert result.output == "geocoding\n"


def test_geocoding_fwd():
    runner = CliRunner()
    result = runner.invoke(
        maps,
        ["tomtom", "geocoding", "--forward", "springfield"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    assert result.output == '{\n  "lat": 37.21552,\n  "lon": -93.29236\n}\n'
    raw_result = runner.invoke(
        maps,
        ["tomtom", "geocoding", "--forward", "springfield", "--raw"],
        catch_exceptions=False,
    )
    assert raw_result.exit_code == 0


def test_geocoding_reverse():
    runner = CliRunner()
    result = runner.invoke(
        maps,
        ["tomtom", "geocoding", "--reverse", "19.16153,72.85618"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    assert "I B Patel Road" in result.output
    raw_result = runner.invoke(
        maps,
        ["tomtom", "geocoding", "--reverse", "19.16153,72.85618", "--raw"],
        catch_exceptions=False,
    )
    assert raw_result.exit_code == 0


def test_geocoding_exception():
    api_key = os.environ["TOMTOM_APIKEY"]
    try:
        del os.environ["TOMTOM_APIKEY"]
        runner = CliRunner()
        result = runner.invoke(
            maps,
            ["tomtom", "geocoding", "--forward", "springfield"],
            catch_exceptions=False,
        )
    finally:
        os.environ["TOMTOM_APIKEY"] = api_key
    assert result.exit_code == 2


def test_mock_display(mocker):
    mocker.patch("maps.tomtom.geo_display", return_value=True)
    runner = CliRunner()
    result = runner.invoke(
        maps,
        ["tomtom", "geocoding", "--forward", "springfield", "--display"],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
