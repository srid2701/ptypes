import attr

from .freqxtime import FreqxTime
from typing import Any, Type, List, TypeVar, Optional


O = TypeVar("O", bound="Observation")


@attr.s(auto_attribs=True)
class Observation(object):

    """"""

    fts: List

    @classmethod
    def fromfils(
        cls: Type[O],
        fnames: List,
    ) -> O:

        """"""

        fts = [FreqxTime.fromfil(fname) for fname in fnames]
        return cls(fts)

    @classmethod
    def fromfits(
        cls: Type[O],
        fnames: List,
    ) -> O:

        """"""

        fts = [FreqxTime.fromfits(fname) for fname in fnames]
        return cls(fts)

    @classmethod
    def fromgups(
        cls: Type[O],
        fnames: List,
    ) -> O:

        """"""

        fts = [FreqxTime.fromgup(fname) for fname in fnames]
        return cls(fts)
