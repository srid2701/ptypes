import attr
import pprint
import typing

from schema import (  # type: ignore
    Or,
    And,
    Schema,
    Optional,
)

from pathlib import Path
from astropy import units as uu  # type: ignore
from astropy.coordinates import SkyCoord  # type: ignore

from .formats import (
    infread,
    infwrite,
    sigread,
    sigwrite,
)


M = typing.TypeVar("M", bound="Metadata")


class NoMeta(Exception):

    """"""

    pass


class Metadata(dict):

    """"""

    def __init__(self, items: typing.Dict = {}):
        super(Metadata, self).__init__(items)

        for key, val in self.items():
            setattr(
                self,
                key,
                val,
            )

    @property
    def coords(self) -> SkyCoord:

        """"""

        try:
            coords = SkyCoord(
                self["raj"],
                self["decj"],
                unit=(uu.hour, uu.degree),
                frame="icrs",
            )
        except KeyError:
            pass

        return coords

    @classmethod
    def frominf(
        cls: typing.Type[M],
        f: str,
    ) -> M:

        """"""

        d = infread(f)
        d["fname"] = f
        return cls.fromdict(d)

    @classmethod
    def fromhdr(
        cls: typing.Type[M],
        f: str,
    ) -> M:

        """"""

        d = sigread(f)
        d["fname"] = f
        return cls.fromdict(d)

    @classmethod
    def fromdict(
        cls: typing.Type[M],
        d: typing.Dict[
            str,
            typing.Any,
        ],
    ) -> M:

        """"""

        return cls(d)

    def toinf(
        self,
        f: typing.Optional[str],
    ) -> None:

        """"""

        attrs = self.todict()
        infwrite(attrs, f)

    def tohdr(
        self,
        f: str,
    ) -> None:

        """"""

        attrs = self.todict()
        sigwrite(attrs, f)

    def todict(self) -> typing.Dict[str, typing.Any]:

        """"""

        return dict(self)
