import pytest

from pathlib import Path
from ptypes.presto import PTypePFD


def test_read(datadir):

    """
    Test reading in a `PFD` file using `PTypePFD`.
    """

    testpath = Path.joinpath(datadir, "test.pfd")

    pfdobj = PTypePFD(testpath)

    assert pfdobj.numdms == 129
    assert pfdobj.numperiods == 129
    assert pfdobj.numpdots == 129
    assert pfdobj.nsub == 128
    assert pfdobj.npart == 60
    assert pfdobj.proflen == 64
    assert pfdobj.numchan == 4096
    assert pfdobj.pstep == 1
    assert pfdobj.pdstep == 2
    assert pfdobj.dmstep == 1
    assert pfdobj.ndmfact == 1
    assert pfdobj.npfact == 1

    assert pfdobj.filename == (
        "fake_noise" ".4096ch" ".8bit" ".J2144-3933" "_DC1" ".fil"
    )

    assert pfdobj.candname == "PSR_2144-3933"
    assert pfdobj.telescope == "GMRT"

    assert pfdobj.pgdev == (
        "fake_noise"
        ".4096ch"
        ".8bit"
        ".J2144-3933"
        "_DC1"
        "_PSR_2144-3933"
        ".pfd"
        ".ps/CPS"
    )

    assert pfdobj.rastr == "21:44:00.0000"
    assert pfdobj.decstr == "-39:33:00.0000"

    assert pytest.approx(pfdobj.tsamp, 0.00016384)
    assert pytest.approx(pfdobj.startT, 0.0)
    assert pytest.approx(pfdobj.endT, 1.0)
    assert pytest.approx(pfdobj.tepoch, 58017.59968182648)
    assert pytest.approx(pfdobj.bepoch, 0.0)
    assert pytest.approx(pfdobj.avgoverc, 0.0)
    assert pytest.approx(pfdobj.lofreq, 300.024926)
    assert pytest.approx(pfdobj.chanwidth, 0.048828)
    assert pytest.approx(pfdobj.bestdm, 2.884502764847447)

    assert pytest.approx(pfdobj.topopow, 0.0)
    assert pytest.approx(pfdobj.topop1, 8.509797317517647)
    assert pytest.approx(pfdobj.topop2, -0.0)
    assert pytest.approx(pfdobj.topop3, 0.0)

    assert pytest.approx(pfdobj.barypow, 0.0)
    assert pytest.approx(pfdobj.baryp1, 0.0)
    assert pytest.approx(pfdobj.baryp2, 0.0)
    assert pytest.approx(pfdobj.baryp3, 0.0)

    assert pytest.approx(pfdobj.foldpow, 0.0)
    assert pytest.approx(pfdobj.foldp1, 0.11751161193245732)
    assert pytest.approx(pfdobj.foldp2, 0.0)
    assert pytest.approx(pfdobj.foldp3, 0.0)

    assert pytest.approx(pfdobj.orbp, 0.0)
    assert pytest.approx(pfdobj.orbe, 0.0)
    assert pytest.approx(pfdobj.orbx, 0.0)
    assert pytest.approx(pfdobj.orbw, 0.0)
    assert pytest.approx(pfdobj.orbt, 0.0)
    assert pytest.approx(pfdobj.orbpd, 0.0)
    assert pytest.approx(pfdobj.orbwd, 0.0)

    assert len(pfdobj.dms) == 129
    assert pytest.approx(pfdobj.dms[0], 0.0)
    assert pytest.approx(pfdobj.dms[-1], 369.2163539004732)

    assert len(pfdobj.periods) == 129
    assert pytest.approx(pfdobj.periods[0], 8.634371343149677)
    assert pytest.approx(pfdobj.periods[-1], 8.388766797914888)

    assert len(pfdobj.pdots) == 129
    assert pytest.approx(pfdobj.pdots[0], 0.0008326328553308873)
    assert pytest.approx(pfdobj.pdots[-1], -0.0008326328553308873)

    assert pfdobj.numprofs == 7680

    assert pfdobj.profs.shape == (60, 128, 64)

    assert pytest.approx(pfdobj.secBINS, 7.520743163677269)
    assert pytest.approx(pfdobj.subCHANS, 32)
    assert pytest.approx(pfdobj.subDFREQ, 1.562496)
    assert pytest.approx(pfdobj.hifreq, 499.97558599999996)
    assert pytest.approx(pfdobj.subLFREQ, 301.538594)

    assert pfdobj.subFREQS.shape == (128,)
    assert pfdobj.subDBINS.shape == (128,)
    assert pfdobj.pointsPERFOLD.shape == (60,)
    assert pfdobj.startSECS.shape == (60,)
    assert pfdobj.midSECS.shape == (60,)


def test_write(datadir, tmp_path):

    """
    Test writing out a `PFD` file using `PTypePFD`.
    We first read in the test file and then write it
    out under the same name but on a temporary path
    made for the purpose. Then we read it in again,
    and compare the two `PTypePFD` objects.
    """

    testpath = Path.joinpath(datadir, "test.pfd")
    fpath = Path.joinpath(tmp_path, "test.pfd")
    pfdobj = PTypePFD(testpath).write(fpath)
    npfdobj = PTypePFD(fpath)
