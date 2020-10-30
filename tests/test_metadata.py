from pathlib import Path
from ptypes.metadata import Metadata  # type: ignore


datadir = Path(__file__).parent.joinpath("data")


def test_inf() -> None:

    """"""

    def check_base(m: Metadata) -> None:

        """"""

        assert m.object == "Pulsar"
        assert m.rastr == "00:00:01.0000"
        assert m.decstr == "-00:00:01.0000"
        assert m.observer == "Kenji Oba"
        assert m.mjd == 59000.0
        assert m.bary == True
        assert m.nsamp == 16
        assert m.tsamp == 6.4e-05
        assert m.analyst == "Space Sheriff Gavan"

    def check_radio(m: Metadata) -> None:

        """"""

        assert m.emband == "Radio"
        assert m.bdiam == 981.0
        assert m.dm == 42.42
        assert m.cfreq == 1182.1953125
        assert m.bw == 400.0
        assert m.nchan == 1024
        assert m.chanwid == 0.390625
        assert m.notes == ["Input filterbank samples have 2 bits."]

    def check_xray(m: Metadata) -> None:

        """"""

        assert m.emband == "X-ray"
        assert m.fov == 3.0
        assert m.cE == 1.0
        assert m.bpE == 5.0
        assert m.notes == ["Full ms-resolution analysis"]
        assert m.onoffs == []

    f = datadir.joinpath("test_fake_presto_radio.inf")
    m = Metadata.frominf(f)

    assert m.bsname == "fake_presto_radio"
    assert m.telescope == "Parkes"
    assert m.instrument == "Multibeam"
    assert m.breaks == False
    assert m.onoffs == []
    check_base(m)
    check_radio(m)

    f = datadir.joinpath("test_fake_presto_radio_breaks.inf")
    m = Metadata.frominf(f)

    assert m.bsname == "fake_presto_radio_breaks"
    assert m.telescope == "Parkes"
    assert m.instrument == "Multibeam"
    assert m.breaks == True
    assert m.onoffs == [(0, 14), (15, 15)]
    check_base(m)
    check_radio(m)

    f = datadir.joinpath("test_fake_presto_xray.inf")
    m = Metadata.frominf(f)

    assert m.bsname == "fake_presto_xray"
    assert m.telescope == "Chandra"
    assert m.instrument == "HRC-S"
    assert m.breaks == False
    check_base(m)
    check_xray(m)


def test_hdr() -> None:

    """"""

    f = datadir.joinpath("test_fake_sigproc_float32.tim")
    m = Metadata.fromhdr(f)

    assert m.source_name == "Pulsar"
    assert m.telescope_id == 4
    assert m.machine_id == 10
    assert m.src_raj == 63642.23
    assert m.src_dej == -454405.0
    assert m.az_start == 0.0
    assert m.za_start == 0.0
    assert m.data_type == 2
    assert m.refdm == 26.31
    assert m.fch1 == 1581.8046875
    assert m.barycentric == 0
    assert m.nchans == 1
    assert m.nbits == 32
    assert m.tstart == 56771.1303125
    assert m.tsamp == 6.4e-05
    assert m.nifs == 1
    assert m.raj == 6.611730555555556
    assert m.decj == -45.734722222222224
    assert m.size == 314


def test_guppi() -> None:

    """"""

    pass
