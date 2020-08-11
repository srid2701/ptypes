import math
import numpy as np

from pathlib import Path
from itertools import zip_longest

from ptypes.consts.tempo import *
from ptypes.core.basis import PType


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
    This will be used to read a single block of data
    in a `POLYCOS` file, in the `PTypePOLYCOS` class.
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

            self.rphase   = float(params[0])
            self.pfreq    = float(params[1])
            self.obsv     = str(params[2])
            self.dataspan = int(params[3])
            self.numcoeff = int(params[4])
            self.obsfreq  = float(params[5])

            try:
                self.binphase = float(params[6])
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
        """

        with open(self.fname, 'r') as infile:

            self.polycos = []
            self.TMIDs   = []

            TPOLY = POLYCO(infile)

            while TPOLY.pulsar:

                self.pulsar = TPOLY.pulsar

                if len(self.polycos):

                    if TPOLY.dataspan != self.dataspan:
                        WARNING = 'Data span is changing!'
                        print(WARNING)

                else:
                    self.dataspan = TPOLY.dataspan

                if TPOLY.pulsar == self.pulsar:
                    self.polycos.append(TPOLY)
                    self.TMIDs.append(TPOLY.TMID)

                TPOLY = POLYCO(infile)

            self.numpoly = len(self.polycos)

            ENDMSG = 'Read {:d} polycos for PSR {:s}.'
            ENDMSG = ENDMSG.format(self.numpoly, self.pulsar)
            print(ENDMSG)
