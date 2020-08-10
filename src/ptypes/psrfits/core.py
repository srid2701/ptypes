import re
import os

import numpy as np
import astropy.units as u
import astropy.coordinates as coord

from pathlib import Path
from astropy.io import fits

from ptypes.core import PType


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


class Spectra(object):

    def __init__(self,
                 freqs,
                 tsamp,
                 data,
                 DM=0,
                 startT=0,
                 endT=1):

        """
        """

        self.data = data.astype('float')

        [self.numchan,
         self.numspec] = self.data.shape

        if len(freqs) != self.numchans:

            ERRMSG = ('Number of observing frequencies '
                      'does not correspond to number of '
                      'channels in the data.')

            raise ValueError(ERRMSG)

        self.freqs  = freqs
        self.tsamp  = tsamp

        self.DM     = DM
        self.startT = startT
        self.endT   = endT

    def __str__(self):
        return str(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def get_chan(self, channum):
        return self.data[channum,:]

    def get_spec(self, specnum):
        return self.data[:,specnum]


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
