import struct
import numpy as np

from pathlib import Path

from ptypes.consts.sigproc import *
from ptypes.core.basis import PType
from ptypes.core.spectra import Spectra


class PTypeFIL(PType):

    """
    """

    def __init__(self,
                 fname):

        """
        """

        super().__init__(fname)

        self.read()

    def read(self):

        """
        """

        pass
