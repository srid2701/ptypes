import pytest

from pathlib import Path


@pytest.fixture(scope='package')
def datadir():

    """
    """

    testsdir = Path(__file__).parent.resolve()
    datadir  = Path.joinpath(testsdir, 'data')
    return datadir
