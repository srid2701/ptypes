import struct
import numpy as np

from pathlib import Path

from ptypes import PType
from ptypes.consts.sigproc import *


class PTypeTIM(PType):

    """
    Class to handle `TIM` files. These files store time
    series, generated by `SIGPROC` in a binary format.
    Every `TIM` file usually has a `SIGPROC` style header
    in it, which stores additional information about the
    time series data. We parse this data with an object
    of the `PTypeHEADER` class.

    This code is borrowed from the `readTim` function of
    Ewan Barr's `sigprocpy`, with apologies. I have just
    cleaned up the code and modified it to work with the
    rest of the package.
    """

    def __init__(self, fname):

        """
        Create an instance of `PTypeTIM`.
        """

        super().__init__(fname)

        self.read()

    def read(self):

        """
        Read a `TIM` file into an instance of PTypeTIM.
        """

        # Read in the `SIGPROC` style header.

        header = PTypeHEADER(self.fname)

        with open(str(self.fname), "rb") as infile:

            # Get the size of the header.

            infile.seek(header.hdrsize)

            # Read data from `TIM` file.
            # Get the `dtype` according
            # to the number of bits.

            self.nbits = header["nbits"]
            self.dtype = NBITStoDTYPE[self.nbits]
            self.data = np.fromfile(infile, dtype=self.dtype)
            self.data = self.data.astype("float32")

        # Set all attributes from header.

        for key, value in header.__dict__.items():
            setattr(self, key, value)
