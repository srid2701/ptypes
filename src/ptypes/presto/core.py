import re
import struct
import numpy as np

from pathlib import Path

from ptypes import PType
from ptypes.consts import *

class PTypeINF(PType):

    """
    Class to handle `INF` files, which store additional
    information about the time series data stored in a
    `DAT` file. These files are human-readable, but this
    class is required to parse the variables from the file.
    This class is be used by class `PTypeDAT`.
    """

    def __init__(self, fname):

        """
        Create an instance of `PTypeINF`.
        """

        super().__init__(fname)

        self.read()

    def read(self):

        """
        Read an `INF` file into an instance of `PTypeINF`.
        """

        INFKEYS = INFtoVARS.keys()
        INFKEYS = list(INFKEYS)

        regex = re.compile(r'''
                           (?P<key>.+)
                           =
                           (?P<value>.+)
                           ''', re.VERBOSE)

        with open(self.fname, 'r') as lines:

            for line in lines:

                if re.search(regex, line):

                    matches = re.search(regex,
                                        line)

                    mdict = matches.groupdict()

                    key   = mdict['key'].strip()
                    value = mdict['value'].strip()

                    if not key in INFKEYS:
                        continue
                    else:

                        [key,
                         ktype] = INFtoVARS[key]

                        setattr(self,
                                key,
                                ktype(value))

class PTypeDAT(PType):

    """
    Class to handle `DAT` files. These files store time
    series in a binary format. Every `DAT` file usually
    has an `INF` file associated with it, which stores
    additional information about the time series data. We
    parse this file with an object of the `PTypeINF` class.
    If the file is absent, an error will be raised.
    """

    def __init__(self,
                 fname,
                 inf=None):

        """
        Create an instance of `PTypeDAT`.
        """

        super().__init__(fname)

        self.read(inf)

    def read(self,
             inf=None):

        """
        Read a `DAT` file into an instance of `PTypeDAT`.

        Inputs:

        inf: str

            The name or path of the corresponding `INF`
            file. If this is set to None, it is asssumed
            that an `INF` file with the same name as the
            `DAT` file exists in the current directory.

            Default: None.
        """

        bsname = Path(self.fname).stem

        if inf is None:
            inf = Path(f'{bsname}.inf')

        if not inf.exists():
            ERROR = 'No corresponding `.inf` file found.'
            raise OSError(ERROR)

        header = PTypeINF(inf)

        with open(self.fname, 'rb') as infile:

            self.data = np.fromfile(infile,
                                    dtype='float32')

        header.inf      = str(inf)
        header.basename = str(bsname)
        header.filename = str(self.fname)
        header.nsamples = self.data.size

        for key, value in header.__dict__.items():
            setattr(self, key, value)

class PTypePFD(PType):

    """
    Class to handle `PFD` (Presto Folded Data) files.
    This stores three-dimensional folded data in a
    binary format. The code is a cleaned-up version of
    the code of the `pfd` class written by Scott Ransom
    in the Python part of the newest release of PRESTO.
    """

    def __init__(self,
                 fname):

        """
        Create an instance of `PTypePFD`.
        """

        super().__init__(fname)

        self.read()

    def _readValues_(self,
                     fobj,
                     numval,
                     btype='int'):

        """
        Private function to read a series of binary values
        of the same format into a list. Uses the `iter_pack`
        method from the `struct` module.

        Inputs:

        fobj: File object.

            An open File object attached to the file from
            which the binary values need to be read.

        numval: int

            Number of values that need to be read.

        btype: str

            The type/format of the binary data that is being
            read.

            Default: 'int'
        """

        values = []

        ctype = FORMATCHARS[btype][0]
        csize = FORMATCHARS[btype][1]

        bufsize = csize * numval

        buffer  = fobj.read(bufsize)

        vtuples = struct.iter_unpack(ctype,
                                     buffer)

        for vtuple in vtuples:
            (value, ) = vtuple
            values.append(value)

        return values

    def _readString_(self,
                     fobj,
                     btype='int'):

        """
        Private function that reads a string from binary
        data. This function also takes care of decoding
        the string into Unicode format (`utf-8`).

        Inputs:

        fobj: File object.

            An open File object attached to the file from
            which the binary string needs to be read.

        btype: str

            The type/format of the binary data that is being
            read.

            Default: 'int'
        """

        ctype = FORMATCHARS[btype][0]
        csize = FORMATCHARS[btype][1]

        (strsize, ) = struct.unpack(ctype,
                                    fobj.read(csize))

        string = fobj.read(strsize)
        string = string.decode('utf-8')

        return string

    def _readArray_(self,
                    fobj,
                    lenarr,
                    btype='double'):

        """
        Private function that reads an array from binary
        data.

        Inputs:

        fobj: File object.

            An open File object attached to the file from
            which the binary array needs to be read.

        lenarr: int

            The length of the array being read.

        btype: str

            The type/format of the binary data that is being
            read.

            Default: 'double'
        """

        ctype = FORMATCHARS[btype][0]
        csize = FORMATCHARS[btype][1]

        cstring = ctype * lenarr

        bufsize = csize * lenarr
        buffer  = fobj.read(bufsize)

        array = struct.unpack(cstring, buffer)

        return array

    def _storeAttrs_(self,
                     keys,
                     values):

        """
        Private function that stores a series of attributes
        into this class. Required since dealing with a large
        number of attributes.

        Inputs:

        keys: iterable

            An iterable over the names of the attributes.

        values: iterable

            An iterable over the values of the attributes.
        """

        for key, value in zip(keys, values):
            setattr(self, key, value)

    def read(self):

        """
        Read a `PFD` file into an instance of `PTypePFD`.
        """

        # WARNING: : No attention has been made
        # to the endianness of the data. Native
        # endianness is assumed. If you are
        # unfortunate enough that you have data
        # from a computer with different endianness
        # from your own, this class can't help you.
        # Yet.

        # TODO: Take care of endianness!

        with open(self.fname, 'rb') as infile:

            # Start reading header parameters
            # from PFD file, and then store
            # them as attributes in this class.

            keys = ['numdms',
                    'numperiods',
                    'numpdots',
                    'nsub',
                    'npart',
                    'proflen',
                    'numchan',
                    'pstep',
                    'pdstep',
                    'dmstep',
                    'ndmfact',
                    'npfact']

            values = self._readValues_(infile, len(keys))
            self._storeAttrs_(keys, values)

            # Stop! Have to process strings differently.
            # Reading:
            #   1. The name of the original file which
            #      was folded.
            #   2. The name of the pulsar candidate.
            #   3. The name of the telescope used for the
            #      the observation.
            #   4. The name of the PostScript file that will
            #      eventually be plotted by `prepfold`.
            #
            # Need to decode the string too.

            keys = ['filename',
                    'candname',
                    'telescope',
                    'pgdev']

            for key in keys:
                string = self._readString_(infile)
                setattr(self, key, string)

            # Stop! Have to process RA and DEC of the
            # observation differently. Have to read
            # the first 16 bytes of the file and test
            # if the coordinates are in a proper format
            # for reading or not, and if there are any
            # coordinates at all. Coordinates might be
            # absent from the file, or simply `Unknown`.

            test = infile.read(16)

            if not test[:8]==b"Unknown" and b':' in test:
                self.rastr = test[:test.find(b'\0')]
                self.rastr = self.rastr.decode('utf-8')

                test = infile.read(16)
                self.decstr = test[:test.find(b'\0')]
                self.decstr = self.decstr.decode('utf-8')
            else:
                self.rastr  = "Unknown"
                self.decstr = "Unknown"

                if ':' not in test:
                    infile.seek(-16, 1)

            # Can start reading attributes the usual
            # way. NOTE: Most attributes from now on
            # are `doubles` rather than `ints`.

            keys = ['tsamp',
                    'startT',
                    'endT',
                    'tepoch',
                    'bepoch',
                    'avgoverc',
                    'lofreq',
                    'chanwidth',
                    'bestdm']

            values = self._readValues_(infile,
                                       len(keys),
                                       btype='double')

            self._storeAttrs_(keys, values)

            # Stop!

            ctype = FORMATCHARS['float'][0]
            csize = FORMATCHARS['float'][1]

            bufsize = csize * 2
            buffer  = infile.read(bufsize)

            (self.topopow, tmp) = struct.unpack(ctype * 2,
                                                buffer)

            keys = ['topop1',
                    'topop2',
                    'topop3']

            values = self._readValues_(infile,
                                       len(keys),
                                       btype='double')

            self._storeAttrs_(keys, values)

            # Stop!

            buffer  = infile.read(bufsize)

            (self.barypow, tmp) = struct.unpack(ctype * 2,
                                                buffer)

            keys = ['baryp1',
                    'baryp2',
                    'baryp3']

            values = self._readValues_(infile,
                                       len(keys),
                                       btype='double')

            self._storeAttrs_(keys, values)

            # Stop!

            buffer  = infile.read(bufsize)

            (self.foldpow, tmp) = struct.unpack(ctype * 2,
                                                buffer)

            keys = ['foldp1',
                    'foldp2',
                    'foldp3']

            values = self._readValues_(infile,
                                       len(keys),
                                       btype='double')

            self._storeAttrs_(keys, values)

            # Can start reading attributes the usual way.

            keys = ['orbp',
                    'orde',
                    'ordx',
                    'ordw',
                    'orbt',
                    'ordpd',
                    'ordwd']

            values = self._readValues_(infile,
                                       len(keys),
                                       btype='double')

            self._storeAttrs_(keys, values)

            # Stop! Need to process arrays now.
            # Reading:
            #   1. The DM axis,
            #   2. The PERIODS axis,
            #   3. The PDOTS axis,
            #
            # NOTE: These arrays are `doubles`.

            arrays = {'dms': self.numdms,
                      'periods': self.numperiods,
                      'pdots': self.numpdots}

            for name, length in arrays.items():
                array = self._readArray_(infile, length)
                setattr(self, name, array)

            self.numprofs = self.nsub*self.npart

            # Stop! Need to read the folded profiles.
            # Folded profiles are 3-dimensional data
            # and have to be read accordingly.

            dimensions = (self.npart,
                          self.nsub,
                          self.proflen)

            self.profs = np.zeros(dimensions, dtype='d')

            pindxs = range(self.npart)
            sindxs = range(self.nsub)

            for pindx in pindxs:
                for sindx in sindxs:

                    self.profs[pindx,
                               sindx,
                               :] = np.fromfile(infile,
                                                np.float64,
                                                self.proflen)

            # NOTE: A `foldstats` struct is read in as a
            # group of 7 doubles that correspond to, in
            # order:
            #   1. numdata
            #   2. data_avg
            #   3. data_var
            #   4. numprof
            #   5. prof_avg
            #   6. prof_var
            #   7. redchi

            numstats = 7
            dimensions = (self.npart,
                          self.nsub,
                          numstats)

            self.stats = np.zeros(dimensions, dtype='d')

            for pindx in pindxs:
                cstats = self.stats[pindx]
                for sindx in sindxs:

                    cstats[sindx] = np.fromfile(infile,
                                                np.float64,
                                                numstats)


class PTypeBESTPROF(PType):

    def __init__(self): pass

class PTypePOLYCOS(PType):

    def __init__(self): pass

class PTypeFFT(PType):

    def __init__(self): pass

class PTypeACCEL(PType):

    def __init__(self): pass
