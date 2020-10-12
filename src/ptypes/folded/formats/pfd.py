import typing
import numpy as np  # type: ignore

from pathlib import Path

from construct import (  # type: ignore
    this,
    Array,
    Struct,
    Int32ul,
    Int32ub,
    Float32l,
    Float32b,
    Float64l,
    Float64b,
    Optional,
    Sequence,
    Computed,
    PascalString,
    PaddedString,
)


pfdstruct = Struct(
    "numdms" / Int32ul,
    "numperiods" / Int32ul,
    "numpdots" / Int32ul,
    "nsub" / Int32ul,
    "npart" / Int32ul,
    "proflen" / Int32ul,
    "numchan" / Int32ul,
    "pstep" / Int32ul,
    "pdstep" / Int32ul,
    "dmstep" / Int32ul,
    "ndmfact" / Int32ul,
    "npfact" / Int32ul,
    "filename" / PascalString(Int32ul, "utf8"),
    "candname" / PascalString(Int32ul, "utf8"),
    "telescope" / PascalString(Int32ul, "utf8"),
    "pgdev" / PascalString(Int32ul, "utf8"),
    "rastr" / PaddedString(16, "utf8"),
    "decstr" / PaddedString(16, "utf8"),
    "tsamp" / Float64l,
    "startT" / Float64l,
    "endT" / Float64l,
    "tepoch" / Float64l,
    "bepoch" / Float64l,
    "avgoverc" / Float64l,
    "lofreq" / Float64l,
    "chanwidth" / Float64l,
    "bestdm" / Float64l,
    "topopow" / Float32l,
    "_t" / Float32l,
    "topop1" / Float64l,
    "topop2" / Float64l,
    "topop3" / Float64l,
    "barypow" / Float32l,
    "_b" / Float32l,
    "baryp1" / Float64l,
    "baryp2" / Float64l,
    "baryp3" / Float64l,
    "foldpow" / Float32l,
    "_f" / Float32l,
    "foldp1" / Float64l,
    "foldp2" / Float64l,
    "foldp3" / Float64l,
    "orbp" / Float64l,
    "orbe" / Float64l,
    "orbx" / Float64l,
    "orbw" / Float64l,
    "orbt" / Float64l,
    "orbpd" / Float64l,
    "orbwd" / Float64l,
    "dms" / Float64l[this.numdms],
    "periods" / Float64l[this.numperiods],
    "pdots" / Float64l[this.numpdots],
    "profs" / Float64l[this.proflen][this.nsub][this.npart],
    "stats" / Float64l[7][this.nsub][this.npart],
    "numprofs" / Computed(this.nsub * this.npart),
)


def pfdread(f: str) -> typing.Dict:

    if Path(f).exists():
        d = pfdstruct.parse_file(f)
        d = dict(d)
        d.pop("_io")

        keys = [
            "dms",
            "pdots",
            "profs",
            "stats",
            "periods",
        ]

        for key in keys:
            d[key] = np.asarray(d[key])

        return d
    else:
        raise OSError("File not found.")


def pfdwrite(
    d: typing.Dict,
    f: str,
) -> None:

    """"""

    pfdstruct.build_file(d, f)
