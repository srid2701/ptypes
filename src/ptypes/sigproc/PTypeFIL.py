import os
import numpy as np

from pathlib import Path

from ptypes import PType
from ptypes.spectra import Spectra
from ptypes.consts.sigproc import *

from .PTypeHEADER import PTypeHEADER

ALLOWED = [8,
           16,
           32]


class PTypeFIL(PType):

    """
    """

    def __init__(self,
                 fname):

        """
        """

        super().__init__(fname)

        header = PTypeHEADER(self.fname)

        for key, value in header.__dict__.items():
            setattr(self, key, value)

        self.freqs = (self.fch1
                      + self.foff
                      * np.arange(self.nchans))

        self.bytespec = (self.nchans
                         * self.nbits
                         // 8)

        self.filsize = os.path.getsize(self.fname)
        self.datsize = self.filsize - self.hdrsize
        self.nspec   = self.datsize // self.bytespec

        NBITS = self.nbits

        if NBITS not in ALLOWED:

            ERRMSG = ('Can only read 8- or 16- bit '
                      'integers, or 32-bit floats. '
                      'The number of bits provided is {}')

            raise ValueError(ERRMSG.format(NBITS))

        else:

            if NBITS != 32:
                DTYPE = ('uint{:d}'
                         .format(NBITS))
                TINFO = np.iinfo(DTYPE)
            else:
                DTYPE = ('float{:d}'
                         .format(NBITS))
                TINFO = np.finfo(DTYPE)

        self.dtype    = DTYPE
        self.dtypeMIN = TINFO.min
        self.dtypeMAX = TINFO.max

    def freqslice(self,
                  START,
                  ISPEC):

        """
        """

        with open(self.fname, 'rb') as infile:

            FREQs  = self.freqs
            TSAMP  = self.tsamp
            NSPECs = self.nspec
            NCHANs = self.nchans
            BYTEs  = self.bytespec

            STARTT = (START * TSAMP)

            WHERE = (START + ISPEC)
            STOP  = min(WHERE, NSPECs)
            POS   = self.hdrsize + (START * BYTEs)

            NSPEC = int(STOP) - int(START)
            NREAD = NSPEC * NCHANs
            NREAD = max(0, NREAD)

            infile.seek(POS,
                        os.SEEK_SET)

            DATA = np.fromfile(infile,
                               count=NREAD,
                               dtype=self.dtype)

            DATA.shape = (NSPEC, NCHANs)

            SPECTRA = Spectra(FREQs,
                              TSAMP,
                              DATA.T,
                              startT=STARTT)

            return SPECTRA

    def timeslice(self,
                  START,
                  STOP):

        """
        """

        with open(self.fname, 'rb') as infile:

            TSAMP = self.tsamp

            START = int(np.round(START/TSAMP))
            STOP  = int(np.round(STOP/TSAMP))

            NSPECs = (STOP - START)

            print(NSPECs)

            SPECTRA = self.freqslice(START, NSPECs)

            return SPECTRA
