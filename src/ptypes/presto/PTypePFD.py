import attr
import typing
import numpy as np  # type: ignore

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

from ptypes.core import PType  # type: ignore

PFDStruct = Struct(
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
    Float32l,
    "topop1" / Float64l,
    "topop2" / Float64l,
    "topop3" / Float64l,
    "barypow" / Float32l,
    Float32l,
    "baryp1" / Float64l,
    "baryp2" / Float64l,
    "baryp3" / Float64l,
    "foldpow" / Float32l,
    Float32l,
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


class PTypePFD(PType):

    """"""

    def __init__(self, fname: str) -> None:

        """"""

        super().__init__(fname)

        self.read()

    def read(self) -> None:

        """"""

        with open(self.fname, "rb") as infile:
            con = PFDStruct.parse_stream(infile)

        self._fromcon(con)
        self._calculate()

    def _fromcon(self, con: typing.MutableMapping) -> None:

        del con["_io"]

        con["dms"] = np.asarray(con["dms"])
        con["pdots"] = np.asarray(con["pdots"])
        con["profs"] = np.asarray(con["profs"])
        con["stats"] = np.asarray(con["stats"])
        con["periods"] = np.asarray(con["periods"])

        for key, value in con.items():
            setattr(self, key, value)

    def _calculate(self) -> None:

        """"""

        pass

    def dedisperse(self) -> None:

        """"""

        pass
