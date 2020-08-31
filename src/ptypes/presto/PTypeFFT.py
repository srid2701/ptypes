import numpy as np

from pathlib import Path

from ptypes import PType
from ptypes.consts.presto import *

from .PTypeINF import PTypeINF

class PTypeFFT(PType):

    """
    Class to handle `FFT` files. These files store Fourier
    series in a binary format. Every `FFT` file usually
    has an `INF` file associated with it, which stores
    additional information about the Fourier series data. We
    parse this file with an object of the `PTypeINF` class.
    If the file is absent, an error will be raised.

    This code is borrowed from the `readFFT` function of
    Ewan Barr's `sigprocpy`, with apologies. I have just
    cleaned up the code and modified it to work with the
    rest of the package.
    """

    def __init__(self,
                 fname,
                 inf=None):

        """
        Create an instance of `PTypeFFT`.
        """

        super().__init__(fname)

        self.read(inf)

    def read(self,
             inf=None):

        """
        Read a `FFT` file into an instance of `PTypeFFT`.

        Inputs:

        inf: str

            The name or path of the corresponding `INF`
            file. If this is set to None, it is asssumed
            that an `INF` file with the same name as the
            `FFT` file exists in the current directory.

            Default: None.
        """

        # Store the basename of the file.

        bsname = Path(self.fname).stem

        # If a separate `INF` file is not specified,
        # look for an `INF` file with the same name
        # as the `FFT` file. Otherwise, an error will
        # be raised.

        if inf is None:
            inf = Path('{}.inf'.format(bsname))
        else:
            inf = Path(inf)

        if not inf.exists():
            ERROR = 'No corresponding `.inf` file found.'
            raise OSError(ERROR)

        # Read `INF` file into an instance of `PTypeINF`.

        header = PTypeINF(inf)

        # Read data from `FFT` file.

        with open(self.fname, 'rb') as infile:

            self.data = np.fromfile(infile,
                                    dtype='float32')

        # Storing some addtional parameters.

        header.inf      = str(inf)
        header.bsname   = str(bsname)
        header.fname    = str(self.fname)
        header.nsamples = self.data.size

        # Set all attributes from `INF` file.

        for key, value in header.__dict__.items():
            setattr(self, key, value)
