import pytest
from click.testing import CliRunner

from bocadillo_cli.main import cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture(name="cli")
def fixture_cli():
    return cli
