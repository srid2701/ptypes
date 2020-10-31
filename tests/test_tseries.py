import tempfile
import numpy as np  # type: ignore

from pathlib import Path
from pytest import raises  # type: ignore
from ptypes.tseries import TimeSeries  # type: ignore


datadir = Path(__file__).parent.joinpath("data")


class TestDat(object):

    """"""

    refdata = np.arange(16)

    def check_data(self, t: TimeSeries) -> None:

        """"""

        assert t.tsamp == 64e-6
        assert t.data.dtype == np.float32
        assert np.allclose(t.data, self.refdata)

    def test_radio(self) -> None:

        """"""

        f = datadir.joinpath("test_fake_presto_radio.dat")
        t = TimeSeries.fromdat(f)
        print(t.data)
        self.check_data(t)

    def test_radio_breaks(self) -> None:

        """"""

        f = datadir.joinpath("test_fake_presto_radio_breaks.dat")
        t = TimeSeries.fromdat(f)
        self.check_data(t)

    def test_xray(self) -> None:

        """"""

        f = datadir.joinpath("test_fake_presto_xray.dat")
        t = TimeSeries.fromdat(f)
        self.check_data(t)

    def test_non_existent(self) -> None:

        """"""

        with raises(FileNotFoundError):
            f = datadir.joinpath("non_existent.dat")
            t = TimeSeries.fromdat(f)

    def test_write(self) -> None:

        """"""

        with tempfile.NamedTemporaryFile(suffix=".dat") as obj:
            dat = Path(obj.name)
            inf = dat.with_suffix(".inf")
            f = datadir.joinpath("test_fake_presto_radio.dat")
            t = TimeSeries.fromdat(f)
            m = t.meta
            m.toinf(inf)
            t.todat(dat)
            test = TimeSeries.fromdat(dat)
            self.check_data(test)


class TestTim(object):

    """"""

    refdata = np.arange(16)

    fnames = [
        "test_fake_sigproc_float32.tim",
        "test_fake_sigproc_uint8.tim",
        "test_fake_sigproc_int8.tim",
    ]

    def test_read(self) -> None:

        """"""

        for fname in self.fnames:
            f = datadir.joinpath(fname)
            t = TimeSeries.fromtim(f)
            assert t.tsamp == 64e-6
            assert t.data.dtype == np.float32
            assert np.allclose(t.data, self.refdata)

    def test_write(self) -> None:

        """"""

        for fname in self.fnames:
            with tempfile.NamedTemporaryFile(suffix=".tim") as obj:
                tim = Path(obj.name)
                f = datadir.joinpath(fname)
                t = TimeSeries.fromtim(f)
                t.totim(tim)
                test = TimeSeries.fromtim(tim)
                assert test.tsamp == 64e-6
                assert test.data.dtype == np.float32
                assert np.allclose(test.data, self.refdata)


def test_npybin() -> None:

    """"""

    tsamp = 64e-6
    refdata = np.arange(16, dtype=np.float32)

    def check_data(t: TimeSeries) -> None:

        """"""

        assert t.tsamp == tsamp
        assert t.data.dtype == np.float32
        assert np.allclose(t.data, refdata)

    t = TimeSeries.fromnpy(refdata, tsamp)
    check_data(t)

    with tempfile.NamedTemporaryFile(suffix=".npy") as f:
        np.save(f.name, refdata)
        t = TimeSeries.fromnpyfile(f.name, tsamp)
        check_data(t)

    with tempfile.NamedTemporaryFile(suffix=".bin") as f:
        refdata.astype(np.float32).tofile(f.name)
        t = TimeSeries.frombin(f.name, np.float32, tsamp)
        check_data(t)
