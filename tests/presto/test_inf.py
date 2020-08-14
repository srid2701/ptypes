import pytest

from pathlib import Path
from ptypes.presto import PTypeINF


def test_read(datadir):

    """
    Test reading in a `INF` file using `PTypeINF`.
    """

    testpath = Path.joinpath(datadir, 'test.inf')

    inf = PTypeINF(testpath)

    assert not inf.breaks
    assert inf.barycentric

    assert inf.fname    == testpath
    assert inf.basename == ('fake_noise'
                               '.4096ch'
                               '.8bit'
                               '.J2144-3933'
                               '_DC1-de-dispersed'
                               '_DM3.35')

    assert inf.telescopeID == 'GMRT'
    assert inf.obstype     == 'Radio'
    assert inf.analyst     == 'guest'
    assert inf.machineID   == 'Unknown'
    assert inf.srcname     == 'J2144-3933'
    assert inf.srcRA       == '21:44:00.0000'
    assert inf.srcDEC      == '-39:33:00.0000'

    assert inf.notes   == [
                                ('Project ID unset, '
                                 'Date: 2017-09-21T14:23:32.5098.'),
                                ('2 polns were summed.  '
                                 'Samples have 8 bits.'),
                             ]

    assert inf.nchan == 4096
    assert inf.nbins == 3600000

    assert pytest.approx(inf.dm, 3.35)
    assert pytest.approx(inf.bw, 199.999488)
    assert pytest.approx(inf.beamdiam, 3600.0)
    assert pytest.approx(inf.chanbw, 0.048828)
    assert pytest.approx(inf.cfreq, 300.024926)
    assert pytest.approx(inf.tsamp, 0.00016384)
    assert pytest.approx(inf.mjd, 58017.604258730986)


def test_write(datadir): pass
