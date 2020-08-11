import struct
import numpy as np

from pathlib import Path

from ptypes import PType
from ptypes.consts.sigproc import *


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
