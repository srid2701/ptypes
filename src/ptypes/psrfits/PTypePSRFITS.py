import re
import os

import numpy as np
import astropy.units as u
import astropy.coordinates as coord

from pathlib import Path
from astropy.io import fits

from ptypes import PType
from ptypes.consts.psrfits import *


def unpack2bit(data):

    """
    """

    pieces = [np.bitwise_and(data >> 0x06, 0x03),
              np.bitwise_and(data >> 0x04, 0x03),
              np.bitwise_and(data >> 0x02, 0x03),
              np.bitwise_and(data >> 0x03)]

    bits = np.dstack(pieces).flatten()

    return bits

def unpack4bit(data):

    """
    """

    pieces = [np.bitwise_and(0x04, 0x0F),
              np.bitwise_and(0x0F)]

    bits = np.dstack(pieces).flatten()

    return bits


class PTypePSRFITS(PType):

    """
    """

    def __init__(self,
                 fname):

        """
        """

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

        """
        """

        pass

    def _readInfo_(self,
                   fobj):

        """
        """

        if not self._isPSRFITS_(fobj):
            ERRMSG = ('File {:s} does not appear to'
                      'be in the PSRFITS format, so'
                      ' cannot read it.')
            raise ValueError(ERRMSG)

        PRIMHDR = fobj['PRIMARY'].header
        SINTHDR = fobj['SUBINT'].header

    def read(self):

        """
        """

        with fits.open(self.fname) as infile:

            pass
