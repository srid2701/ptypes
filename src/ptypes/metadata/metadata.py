import attr
import typing

from pathlib import Path
from astropy import units as uu  # type: ignore
from astropy.coordinates import SkyCoord  # type: ignore


@attr.s(auto_attribs=True)
class Metadata(dict):

    """"""

    def frominf():
        pass

    def fromhdr():
        pass

    def fromdict():
        pass

    def toinf():
        pass

    def tohdr():
        pass

    def todict():
        pass
