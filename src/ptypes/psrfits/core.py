import re
import os

import numpy as np
import astropy.units as u
import astropy.coordinates as coord

from pathlib import Path
from astropy.io import fits

class PTypePSRFITS(PType):

    def __init__(self,
                 fname):

        super().__init__(fname)

        self.read()

    def __readSubInt__(self,
                       isub,
                       scales=True,
                       offsets=True,
                       weights=True,
                       zerooff=True,
                       collapse=True):

        pass

    def read(self):

        with fits.open(self.fname) as infile:

            pass
