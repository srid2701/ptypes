import attr
import typing
import numpy as np  # type: ignore

from pathlib import Path
from ptypes.metadata import Metadata

from .formats import (
    fftread,
    fftwrite,
    specread,
    specwrite,
)


@attr.s(auto_attribs=True)
class Fourier(object):

    """"""

    def fromnpy():
        pass

    def fromfft():
        pass

    def fromspec():
        pass

    def tonpy():
        pass

    def tofft():
        pass

    def tospec():
        pass
