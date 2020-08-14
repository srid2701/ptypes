import pytest

from pathlib import Path
from ptypes.presto import PTypeDAT


def test_read(datadir):

    """
    Test reading in a `DAT` file using `PTypeDAT`.
    """

    testpath = Path.joinpath(datadir, 'test.dat')

    infpath  = testpath.with_suffix('.inf')

    dat = PTypeDAT(testpath,
                   inf=infpath)

    assert dat.nsamples   == 3600000
    assert dat.data.shape == (3600000,)
    assert dat.data.shape == (dat.nsamples,)

    assert pytest.approx(dat.data[0], 127869.0)
    assert pytest.approx(dat.data[-1], 127869.0)

    assert dat.bsname == 'test'

    assert dat.inf   == str(infpath)
    assert dat.fname == str(testpath)


def test_write(datadir):

    pass
