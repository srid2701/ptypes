import pytest

from pathlib import Path
from ptypes.presto import PTypeBESTPROF


def test_read(datadir):

    """
    Test reading in a `BESTPROF` file using `PTypeBESTPROF`.
    """

    testpath = Path.joinpath(datadir, "test.pfd.bestprof")

    bprof = PTypeBESTPROF(testpath)

    assert not bprof.wrad
    assert not bprof.porb
    assert not bprof.tperi
    assert not bprof.asinc
    assert not bprof.eccen
    assert not bprof.pbary
    assert not bprof.epbary
    assert not bprof.pdbary
    assert not bprof.pddbary

    assert bprof.nbins == 64

    assert bprof.fname == ("fake_noise" ".4096ch" ".8bit" ".J2144-3933" "_DC1" ".fil")

    assert bprof.telescope == "GMRT"
    assert bprof.candname == "PSR_2144-3933"

    assert pytest.approx(bprof.dm, 2.885)
    assert pytest.approx(bprof.pdtopo, -0.0)
    assert pytest.approx(bprof.pddtopo, 0.0)
    assert pytest.approx(bprof.nsamp, 3600000.0)
    assert pytest.approx(bprof.ptopoerr, 0.0272)
    assert pytest.approx(bprof.tsamp, 0.00016384)
    assert pytest.approx(bprof.chisqr, 22415.146)
    assert pytest.approx(bprof.pdtopoerr, 3.92e-09)
    assert pytest.approx(bprof.pddtopoerr, 3.92e-09)
    assert pytest.approx(bprof.davg, 127025.959584786)
    assert pytest.approx(bprof.dstd, 211.244531615612)
    assert pytest.approx(bprof.ptopo, 8509.79731751765)
    assert pytest.approx(bprof.eptopo, 58017.59968182648)
    assert pytest.approx(bprof.profavg, 7113256675.58816)
    assert pytest.approx(bprof.profstd, 50101.0397370587)
