import attr
import typing

from construct import (  # type: ignore
    this,
    Probe,
    Switch,
    Struct,
    Int8ul,
    Int8ub,
    Int32ul,
    Int32ub,
    Float32l,
    Float32b,
    Float64l,
    Float64b,
    GreedyRange,
    PascalString,
)

from ptypes.core import PType  # type: ignore
from ptypes.consts.sigproc import *


DEFAULT = "Unknown"


KeyStruct = Struct(
    "key" / PascalString(Int32ul, "utf8"),
    "value"
    / Switch(
        this.key,
        SIGPROCKEYS,
    ),
)


SIGPROCStruct = Struct(
    "attrs" / GreedyRange(KeyStruct),
)


class PTypeHEADER(PType):

    """"""

    def __init__(self, fname: str) -> None:

        """"""

        super().__init__(fname)

        self.read()

    def read(self) -> None:

        """"""

        with open(self.fname, "rb") as infile:
            con = SIGPROCStruct.parse_stream(infile)
            self.hdrsize = infile.tell()

        self._fromcon(con)

    def _fromcon(
        self,
        con: typing.MutableMapping,
    ) -> None:

        """"""

        del con["_io"]

        attrs = con["attrs"]

        for attribute in attrs:
            setattr(
                self,
                attribute["key"],
                attribute["value"],
            )

        self.telescope = IDtoTELESCOPE.get(
            self.telescope_id,
            DEFAULT,
        )

        self.machine = IDtoMACHINE.get(
            self.machine_id,
            DEFAULT,
        )

        self.dtype = DATATYPES.get(
            self.data_type,
            DEFAULT,
        )
