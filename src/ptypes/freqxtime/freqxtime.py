import attr
import numpy as np  # type: ignore

from ptypes.metadata import NoMeta, Metadata
from typing import Any, Type, List, Dict, Tuple, TypeVar, Optional


FT = TypeVar("FT", bound="FreqxTime")


@attr.s(auto_attribs=True)
class FreqxTime(object):

    nchan: int
    nsamp: int
    meta: Optional[Metadata] = None
    data: Optional[np.ndarray] = None

    @classmethod
    def fromnpy(
        cls: Type[FT],
        array: np.ndarray,
    ) -> FT:

        """"""

        if len(array.shape) != 2:
            errmsg = "Initialising array must be two-dimensional! Exiting!"
            raise ValueError(errmsg)

        nchan = array.shape(0)
        nsamp = array.shape(1)

        return cls(
            data=array,
            nchan=nchan,
            nsamp=nsamp,
        )

    @classmethod
    def fromfil(
        cls: Type[FT],
        fname: str,
    ) -> FT:

        """"""

        meta = Metadata.fromhdr(fname)

        try:
            nsamp = meta["nsamp"]
            nchan = meta["nchan"]
        except KeyError:
            raise NoMeta("Metadata missing! Exiting...")

        return cls(
            nchan=nchan,
            nsamp=nsamp,
            meta=meta,
        )

    @classmethod
    def fromfits(
        cls: Type[FT],
        fname: str,
    ) -> FT:

        """"""

        meta = Metadata.fromfits(fname)

        try:
            nchan = meta["nchan"]
            nsamp = meta["nsamp"]
        except KeyError:
            raise NoMeta("Metadata missing! Exiting...")

        return cls(
            nchan=nchan,
            nsamp=nsamp,
            meta=meta,
        )

    @classmethod
    def fromgup(
        cls: Type[FT],
        fname: str,
    ) -> FT:

        """"""

        meta = Metadata.fromgup(fname)

        try:
            nchan = meta["nchan"]
            nsamp = meta["nsamp"]
        except KeyError:
            raise NoMeta("Metadata missing! Exiting...")

        return cls(
            nchan=nchan,
            nsamp=nsamp,
            meta=meta,
        )
