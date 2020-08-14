import pytest

from pathlib import Path
from ptypes.sigproc import PTypeFIL


def test_read(datadir):

    """
    Test reading in a `FIL` file using `PTypeFIL`.
    """

    testpath = Path.joinpath(datadir, 'test.fil')

    fil = PTypeFIL(testpath)

    spectra = fil.freqslice(0, 5120)

    assert spectra.data.shape == (336, 5120)

    assert pytest.approx(spectra.data[0][0], 165.0)
    assert pytest.approx(spectra.data[335][5119], 126.0)
