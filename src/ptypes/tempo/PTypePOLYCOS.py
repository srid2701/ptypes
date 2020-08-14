import math
import numpy as np

from pathlib import Path
from itertools import zip_longest

from ptypes import PType
from ptypes.consts.tempo import *


DOT    = '.'
HYP    = '-'
DOPFAC = 1e-4

def padder(matrix):

    """
    Pad a matrix with zeroes if it is missing
    some values, and put it all in a 2-D numpy
    array. This converts a 2-D array which has
    unequal number of values in some rows to a
    square matrix.

    Input(s):

    matrix: list of lists, or numpy array.

        A 2-D array of values. This is not
        a matrix yet, because the rows have
        unequal number of values.

    Output(s):

    array: numpy array

        A 2-D numpy array, with all missing
        values filled with zeroes to form a
        square matrix.
    """

    array = np.array(list(zip_longest(*matrix,
                                      fillvalue=0))).T
    return array

class POLYCO(object):

    """
    This will be used to read a single block of data in a
    `POLYCOS` file, in the `PTypePOLYCOS` class. Polynomial
    ephemerides for a pulsar are stored in a sequence. This
    class represents just a single block from such a sequence.
    Each block has the following format:

    Line  Columns     Item
    ----  -------   -----------------------------------
      1      1-10   Pulsar Name
            11-19   Date (dd-mmm-yy)
            20-31   UTC (hhmmss.ss)
            32-51   TMID (MJD)
            52-72   DM
            74-79   Doppler shift due to earth motion (10^-4)
            80-86   Log_10 of fit rms residual in periods
      2      1-20   Reference Phase (RPHASE)
            21-38   Reference rotation frequency (F0)
            39-43   Observatory number (see note ** below)
            44-49   Data span (minutes)
            50-54   Number of coefficients
            55-75   Observing frequency (MHz)
            76-80   Binary phase
      3*     1-25   Coefficient 1 (COEFF(1))
            26-50   Coefficient 2 (COEFF(2))
            51-75   Coefficient 3 (COEFF(3))

    *  Subsequent lines have three coefficients each, up to NCOEFF
    ** Observatory numbers are integers based on the observatory code.
    """

    def __init__(self,
                 fobj):

        """
        Create a `POLYCO` instance.
        """

        self.read(fobj)

    def read(self,
             fobj):

        """
        Read a a single block of data into a `POLYCO` instance.
        """

        fline  = fobj.readline()

        if fline is '':
            self.pulsar = None
        else:

            params = fline.split()

            self.pulsar = str(params[0])
            self.date   = str(params[1])
            self.UTC    = str(params[2])
            self.TMID   = float(params[3])
            self.DM     = float(params[4])

            [self.TMIDf,
             self.TMIDi] = math.modf(self.TMID)

            self.TMIDi = int(self.TMIDi)
            self.TMIDf = float(self.TMIDf)

            try:

                self.doppler  = float(params[5]) * DOPFAC
                self.log10rms = float(params[6])

            except IndexError:

                self.log10rms = params[-1].split(HYP)[-1]
                self.log10rms = ''.join([HYP, self.log10rms])

                slicer = params[-1].find(self.log10rms)

                self.doppler  = params[-1][:slicer]
                self.doppler  = float(self.doppler)
                self.log10rms = float(self.log10rms)

            line   = fobj.readline()
            params = line.split()

            self.refPhase = float(params[0])
            self.refFreq  = float(params[1])
            self.obsv     = str(params[2])
            self.dataSpan = int(params[3])
            self.numCoeff = int(params[4])
            self.obsFreq  = float(params[5])

            try:
                self.binPhase = float(params[6])
            except IndexError:
                pass

            MAT = []

            while True:

                line   = fobj.readline()
                params = line.split()

                if (len(params) > 3) or (len(params) == 0):
                    fobj.seek(position)
                    break
                else:
                    position = fobj.tell()

                COEFFS = []

                for param in params:
                    param  = param.replace('D', 'E')
                    COEFFS.append(float(param))

                MAT.append(COEFFS)

            MAT = padder(MAT)

            self.coeffs = MAT.reshape(-1)

            self.phasepoly = (np
                              .polynomial
                              .polynomial
                              .Polynomial(self.coeffs))


class PTypePOLYCOS(PType):

    """
    Class to handle 'POLYCOS' files, which store the
    polynomial ephemerides for a pulsar. This data is
    usually written by `TEMPO`, one of the most widely
    used programs for pulsar timing, to a file named
    `polycos.dat`. These polynomials are used to get
    predictions for the frequency and phase of the
    pulsar via the formulas:

    DT = (T-TMID) * 1440

    PHASE = (RPHASE
             + DT*60*F0
             + COEFF(1)
             + DT*COEFF(2)
             + DT^2*COEFF(3)
             + ....)

    FREQ(Hz) = (F0
                + (1/60)*(COEFF(2)
                + 2*DT*COEFF(3)
                + 3*DT^2*COEFF(4)
                + ....)
    """

    def __init__(self,
                 fname):

        """
        Create an instance of `PTypePOLYCOS`.
        """

        super().__init__(fname)

        self.read()

    def read(self):

        """
        Read a `POLYCOS` file into an instance of `PTypePOLYCOS`.
        """

        with open(self.fname, 'r') as infile:

            self.polycos = []
            self.TMIDs   = []

            TPOLY = POLYCO(infile)

            while TPOLY.pulsar:

                self.pulsar = TPOLY.pulsar

                if len(self.polycos):

                    if TPOLY.dataspan != self.dataSpan:
                        WARNING = 'Data span is changing!'
                        print(WARNING)

                else:
                    self.dataSpan = TPOLY.dataspan

                if TPOLY.pulsar == self.pulsar:
                    self.polycos.append(TPOLY)
                    self.TMIDs.append(TPOLY.TMID)

                TPOLY = POLYCO(infile)

            self.numpoly = len(self.polycos)

            ENDMSG = 'Read {:d} polycos for PSR {:s}.'
            ENDMSG = ENDMSG.format(self.numpoly, self.pulsar)
            print(ENDMSG)
