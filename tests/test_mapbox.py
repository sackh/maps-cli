"""Module to test MapBox services."""
import os

from click.testing import CliRunner

from maps.commands import maps


def test_show():
    """Test mapbox show command."""
    runner = CliRunner()
    result = runner.invoke(maps, ["mapbox", "show"], catch_exceptions=False)
    assert result.output == "geocoding\nisochrone\nmatrix\n"


def test_geocoding_fwd():
    runner = CliRunner()
    result = runner.invoke(
        maps, ["mapbox", "geocoding", "--forward", "springfield"], catch_exceptions=False
    )
    assert result.exit_code == 0
    assert result.output == '{\n  "lat": 37.2153,\n  "lon": -93.2983\n}\n'
    raw_result = runner.invoke(
        maps, ["mapbox", "geocoding", "--forward", "springfield", "--raw"], catch_exceptions=False
    )
    assert raw_result.exit_code == 0


def test_geocoding_reverse():
    runner = CliRunner()
    result = runner.invoke(
        maps, ["mapbox", "geocoding", "--reverse", "19.16153,72.85618"], catch_exceptions=False
    )
    assert result.exit_code == 0
    assert "Haptik, 8th Floor" in result.output
    raw_result = runner.invoke(
        maps,
        ["mapbox", "geocoding", "--reverse", "19.16153,72.85618", "--raw"],
        catch_exceptions=False,
    )
    assert raw_result.exit_code == 0


def test_geocoding_exception():
    api_key = os.environ["MAPBOX_APIKEY"]
    try:
        del os.environ["MAPBOX_APIKEY"]
        runner = CliRunner()
        result = runner.invoke(
            maps, ["mapbox", "geocoding", "--forward", "springfield"], catch_exceptions=False
        )
    finally:
        os.environ["MAPBOX_APIKEY"] = api_key
    assert result.exit_code == 2


def test_isochrone():
    runner = CliRunner()
    result = runner.invoke(
        maps,
        [
            "mapbox",
            "isochrone",
            "--profile=driving",
            "--coordinates=-118.22258,33.99038",
            "--contours_minutes=5",
            "--contours_colors=6706ce",
            "--polygons",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    assert "FeatureCollection" in result.output


def test_isochrone_exception():
    api_key = os.environ["MAPBOX_APIKEY"]
    try:
        del os.environ["MAPBOX_APIKEY"]
        runner = CliRunner()
        result = runner.invoke(
            maps,
            [
                "mapbox",
                "isochrone",
                "--profile=driving",
                "--coordinates=-118.22258,33.99038",
                "--contours_minutes=5",
                "--contours_colors=6706ce",
                "--polygons",
            ],
            catch_exceptions=False,
        )
    finally:
        os.environ["MAPBOX_APIKEY"] = api_key
    assert result.exit_code == 2


def test_matrix():
    runner = CliRunner()
    result = runner.invoke(
        maps,
        [
            "mapbox",
            "matrix",
            "--profile=driving",
            "--coordinates=-122.42,37.78;-122.45,37.91;-122.48,37.73",
            "--annotations=distance,duration",
            "--approaches=curb;curb;curb",
            "--destinations=all",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    assert '"code": "Ok"' in result.output


def test_matrix_exception():
    api_key = os.environ["MAPBOX_APIKEY"]
    try:
        del os.environ["MAPBOX_APIKEY"]
        runner = CliRunner()
        result = runner.invoke(
            maps,
            [
                "mapbox",
                "matrix",
                "--profile=driving",
                "--coordinates=-122.42,37.78;-122.45,37.91;-122.48,37.73",
                "--annotations=distance,duration",
                "--approaches=curb;curb;curb",
                "--destinations=all",
            ],
            catch_exceptions=False,
        )
    finally:
        os.environ["MAPBOX_APIKEY"] = api_key
    assert result.exit_code == 2


def test_mock_display(mocker):
    mocker.patch("maps.mapbox.geo_display", return_value=True)
    runner = CliRunner()
    result = runner.invoke(
        maps,
        [
            "mapbox",
            "isochrone",
            "--profile=driving",
            "--coordinates=-118.22258,33.99038",
            "--contours_minutes=5",
            "--contours_colors=6706ce",
            "--polygons",
            "--display",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0
    runner = CliRunner()
    result = runner.invoke(
        maps,
        ["mapbox", "geocoding", "--forward", "springfield", "--display"],
        catch_exceptions=False,
    )
