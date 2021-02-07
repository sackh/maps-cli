"""Test maps main command group."""
from click.testing import CliRunner

from maps import __version__
from maps.commands import maps


def test_version():
    assert __version__ == "0.0.2"


def test_show():
    """Test osm show command."""
    runner = CliRunner()
    result = runner.invoke(maps, ["show"], catch_exceptions=False)
    assert result.output.split() == ["osm", "here", "mapbox", "tomtom"]
