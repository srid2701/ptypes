import re
import os

import numpy as np
import astropy.units as u
import astropy.coordinates as coord

from pathlib import Path
from astropy.io import fits

from ptypes.consts.psrfits import *
from ptypes.core.basis import PType
from ptypes.core.spectra import Spectra


def unpack2bit(data):

    pieces = [np.bitwise_and(data >> 0x06, 0x03),
              np.bitwise_and(data >> 0x04, 0x03),
              np.bitwise_and(data >> 0x02, 0x03),
              np.bitwise_and(data >> 0x03)]

    bits = np.dstack(pieces).flatten()

    return bits

def unpack4bit(data):

    pieces = [np.bitwise_and(0x04, 0x0F),
              np.bitwise_and(0x0F)]

    bits = np.dstack(pieces).flatten()

    return bits


class PTypePSRFITS(PType):

    BYTESIZE = 8

    def __init__(self,
                 fname):

        super().__init__(fname)

        self.read()

    def _readSubInt_(self,
                     fobj,
                     isub,
                     scales=True,
                     offsets=True,
                     weights=True,
                     zerooff=True,
                     collapse=True):

        pass

    def _readInfo_(self): pass

    def read(self):

        with fits.open(self.fname) as infile:

            pass
