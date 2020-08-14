import pytest

from pathlib import Path
from ptypes.presto import PTypeFFT


def test_read(datadir):

    """
    Test reading in a `FFT` file using `PTypeFFT`.
    """

    testpath = Path.joinpath(datadir, 'test.fft')

    infpath  = testpath.with_suffix('.inf')

    fft = PTypeFFT(testpath,
                      inf=infpath)

    assert fft.nsamples   == 3600000
    assert fft.data.shape == (3600000,)
    assert fft.data.shape == (fft.nsamples,)

    assert pytest.approx(fft.data[0], 457293100000.0)
    assert pytest.approx(fft.data[-1], -235820.34)

    assert fft.bsname == 'test'

    assert fft.inf   == str(infpath)
    assert fft.fname == str(testpath)



def test_write(datadir):

    pass
