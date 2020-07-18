import numpy as np

from pathlib import Path

from ptypes import PType
from ptypes.consts import *

class PTypeINF(PType):

    def __init__(self, fname):

        super().__init__(fname,
                         nbits=None)

        self.read()

    def read(self):

        """
        """

        INFKEYS = INFtoVARS.keys()
        INFKEYS = list(INFKEYS)

        with open(self.fname, 'r') as lines:
            for line in lines:
                field = line.split('=')
                key   = field[0].strip()
                value = field[-1].strip()

                if not key in INFKEYS:
                    continue
                else:

                    [key,
                     ktype] = INFtoVARS[key]

                    setattr(self,
                            key,
                            ktype(value))

class PTypeDAT(PType):

    def __init__(self,
                 fname,
                 inf=None,
                 nbits=32):

        super().__init__(fname,
                         nbits)

        self.read(inf)

    def read(self,
             inf=None):

        """
        """

        self.dtype = NBITStoDTYPE[self.nbits]

        bsname = Path(self.fname).stem

        if inf is None:
            inf = Path(f'{bsname}.inf')

        if not inf.exists():
            ERROR = 'No corresponding `.inf` file found.'
            raise OSError(ERROR)

        header = PTypeINF(inf)

        with open(self.fname, 'rb') as infile:

            self.data = np.fromfile(infile,
                                    dtype=self.dtype)

        header.inf      = str(inf)
        header.basename = str(bsname)
        header.filename = str(self.fname)
        header.nsamples = self.data.size

        for key, value in header.__dict__.items():
            setattr(self, key, value)

class PTypePFD(PType):

    def __init__(self): pass

class PTypeBESTPROF(PType):

    def __init__(self): pass

class PTypePOLYCOS(PType):

    def __init__(self): pass

class PTypeFFT(PType):

    def __init__(self): pass

class PTypeACCEL(PType):

    def __init__(self): pass
