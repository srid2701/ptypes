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


schs = {
    Optional("source_name"): Or(str, None),
    Optional("coords"): Or(SkyCoord, None),
    Optional("dm"): Or(And(float, lambda x: x >= 0), None),
    Optional("mjd"): Or(And(float, lambda x: x >= 0), None),
    Optional("tobs"): Or(And(float, lambda x: x > 0), None),
    Optional("fname"): Or(str, None),
}

metama = Schema(schs, ignore_extra_keys=True)


class Metadata(dict):

    """"""

    def __init__(self, items: typing.Dict = {}):
        metama.validate(items)
        super(Metadata, self).__init__(items)

        for sch in schs:
            if isinstance(sch.schema, str):
                self.setdefault(sch.schema, None)

        self._classlike()

    def _classlike(self) -> None:

        """"""

        for key, val in self.items():
            setattr(
                self,
                key,
                val,
            )

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

        try:
            d["coords"] = SkyCoord(
                d["raj"],
                d["decj"],
                unit=(uu.hour, uu.degree),
                frame="icrs",
            )
        except KeyError:
            pass

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
        f: typing.Optional[str],
    ) -> None:

        """"""

        attrs = self.todict()
        sigwrite(attrs, f)

    def todict(self) -> typing.Dict[str, typing.Any]:

        """"""

        return dict(self)
