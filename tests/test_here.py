"""Module to test HERE services."""
import json

from click.testing import CliRunner

from maps.commands import maps


def test_show():
    """Test here show command."""
    runner = CliRunner()
    result = runner.invoke(maps, ["here", "show"], catch_exceptions=False)
    assert result.output.split() == ["geocoding", "discover"]


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


def test_discover():
    runner = CliRunner()
    result = runner.invoke(
        maps,
        ["here", "discover", "starbucks", "--coordinates=72.8526,19.1663", "--country_codes=IND"],
    )
    assert result.exit_code == 0
    assert "Starbucks, New Link Road, Andheri West, Mumbai 400053, India" in result.output

    result2 = runner.invoke(
        maps,
        [
            "here",
            "discover",
            "coffee",
            "--coordinates=13.38469,52.53086",
            "--radius=1000",
            "--raw",
        ],
    )
    assert result2.exit_code == 0
    assert '"title": "Eins"' in result2.output

    result3 = runner.invoke(
        maps,
        [
            "here",
            "discover",
            "starbucks",
            "--bounding_box=13.08836,52.33812,13.761,52.6755",
            "--limit=1",
            "--lang=en-US",
        ],
    )
    assert result3.exit_code == 0
    assert "Starbucks, Am Ostbahnhof, 10243 Berlin, Germany" in result3.output
