import tempfile
import numpy as np  # type: ignore

from pathlib import Path
from ptypes.tseries import TimeSeries  # type: ignore


datadir = Path(__file__).parent.joinpath("data")


def test_dat() -> None:

    """"""

    def check_data(
        t: TimeSeries,
        refdata: np.ndarray,
    ) -> None:

        """"""

        assert t.tsamp == 64e-6
        assert t.data.dtype == np.float32
        assert np.allclose(t.data, refdata)

    refdata = np.arange(16)

    f = datadir.joinpath("test_fake_presto_radio.dat")
    t = TimeSeries.fromdat(f)
    print(t.data)
    check_data(t, refdata)

    f = datadir.joinpath("test_fake_presto_radio_breaks.dat")
    t = TimeSeries.fromdat(f)
    check_data(t, refdata)

    f = datadir.joinpath("test_fake_presto_xray.dat")
    t = TimeSeries.fromdat(f)
    check_data(t, refdata)


def test_tim() -> None:

    """"""

    refdata = np.arange(16)
    fnames = [
        "test_fake_sigproc_float32.tim",
        "test_fake_sigproc_uint8.tim",
        "test_fake_sigproc_int8.tim",
    ]

    for fname in fnames:
        f = datadir.joinpath(fname)
        t = TimeSeries.fromtim(f)
        assert t.tsamp == 64e-6
        assert t.data.dtype == np.float32
        assert np.allclose(t.data, refdata)


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
