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
    class is required to parse the variables.

    This class is used with class `PTypeDAT`.
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

        # Regular expression to parse keys
        # and values from an INF file.

        regex = re.compile(r'''
                           (?P<key>.+)      # The key.
                           =                # The separator.
                           (?P<value>.+)    # The value.
                           ''', re.VERBOSE)

        with open(self.fname, 'r') as lines:

            # Initialise empty list to store
            # the additional notes at the end
            # of the file.

            notes = []

            for line in lines:

                if re.search(regex, line):

                    # Get all keys and parameters.
                    # The `=` sign is the separator
                    # here. Use regular expressions
                    # to parse the file.

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

                else:

                    # Append additional notes.

                    notes.append(line)

            # Clip the heading from additional notes
            # at the end of the INF file, and then
            # store them in the `notes` attribute.

            notes = notes[1:]
            notes = [note.strip()
                     for note in notes]
            notes = [note
                     for note in notes
                     if note]

            setattr(self,
                    'notes',
                    notes)

class PTypeDAT(PType):

    """
    Class to handle `DAT` files. These files store time
    series, generated by `PRESTO` in a binary format.
    Every `DAT` file usually has an `INF` file associated
    with it, which stores additional information about the
    time series data. We parse this file with an object of
    the `PTypeINF` class. If the file is absent, an error
    will be raised.

    This code is borrowed from the `readDat` function of
    Ewan Barr's `sigprocpy`, with apologies. I have just
    cleaned up the code and modified it to work with the
    rest of the package.
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

        # Store the basename of the file.

        bsname = Path(self.fname).stem

        # If a separate `INF` file is not specified,
        # look for an `INF` file with the same name
        # as the `DAT` file. Otherwise, an error will
        # be raised.

        if inf is None:
            inf = Path(f'{bsname}.inf')

        if not inf.exists():
            ERROR = 'No corresponding `.inf` file found.'
            raise OSError(ERROR)

        # Read `INF` file into an instance of `PTypeINF`.

        header = PTypeINF(inf)

        # Read data from `DAT` file.

        with open(self.fname, 'rb') as infile:

            self.data = np.fromfile(infile,
                                    dtype='float32')

        # Storing some addtional parameters.

        header.inf      = str(inf)
        header.basename = str(bsname)
        header.filename = str(self.fname)
        header.nsamples = self.data.size

        # Set all attributes from `INF` file.

        for key, value in header.__dict__.items():
            setattr(self, key, value)


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
        Create an instance of `PTypeDAT`.
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
            inf = Path(f'{bsname}.inf')

        if not inf.exists():
            ERROR = 'No corresponding `.inf` file found.'
            raise OSError(ERROR)

        # Read INF file into an instance of `PTypeINF`.

        header = PTypeINF(inf)

        # Read data from `FFT` file.

        with open(self.fname, 'rb') as infile:

            self.data = np.fromfile(infile,
                                    dtype='float32')

        # Storing some addtional parameters.

        header.inf      = str(inf)
        header.basename = str(bsname)
        header.filename = str(self.fname)

        # Set all attributes from `INF` file.

        for key, value in header.__dict__.items():
            setattr(self, key, value)


class PTypePFD(PType):

    BPROFEXT   = '.bestprof'
    POLYCOSEXT = '.polycos'

    """
    Class to handle `PFD` (Presto Folded Data) files.
    This stores three-dimensional folded data in a
    binary format.

    This code is a cleaned-up version of the code of the
    `pfd` class written by Scott Ransom in the Python part
    of the newest release (v3.0.1) of `PRESTO`.
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

        (ctype,
         csize) = FORMATCHARS[btype]

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

        (ctype,
         csize) = FORMATCHARS[btype]

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

        (ctype,
         csize) = FORMATCHARS[btype]

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

        # WARNING: No attention has been made to the
        # endianness of the data. Native endianness is
        # assumed. If you are unfortunate enough that
        # you have data from a computer with different
        # endianness from your own, this class can't
        # help you. Yet.

        # TODO: Take care of endianness!

        with open(self.fname, 'rb') as infile:

            # Try to read the `BESTPROF` file.

            try:

                bprofname = ''.join([self.fname,
                                     self.BPROFEXT])

                self.bestprof = PTypeBESTPROF(bprofname)

            except OSError:

                self.bestprof = None

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

            (ctype,
             csize) = FORMATCHARS['float']

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


class PTypeACCEL(PType):

    def __init__(self): pass


class PTypeBESTPROF(PType):

    """
    Class to handle `BESTPROF` files, which store the
    best profile of a particular candidate folded using
    `PRESTO`. These files are human-readable, but this
    class is required to parse the variables.

    This class is used with class 'PTypePFD'.
    """

    def __init__(self, fname):

        """
        Create an instance of `PTypeBESTPROF`.
        """

        super().__init__(fname)

        self.read()

    def read(self):

        """
        Read an `BESTPROF` file into an instance
        of `PTypeBESTPROF`.
        """

        BESTPROFKEYS = BESTPROFtoVARS.keys()
        BESTPROFKEYS = list(BESTPROFKEYS)

        with open(self.fname, 'r') as infile:

            lines = infile.read()

            # Regular expression to separate header
            # and data in a `BESTPROF` file.

            regex = re.compile(r'\#{2,}')

            # Separate header and data.

            [header,
             data] = re.split(regex, lines)

            # Split data along newline
            # characters.

            data = re.split(r'\n+',
                            data)

            for indx, line in enumerate(data):

                number = line.strip()
                point  = re.split(r'\s+',
                                  number)[-1]
                data[indx] = point

            # Remove empties from data.

            data = [number
                    for number in data
                    if number]

            # Type convert data to a `numpy`
            # array and store it in this class
            # as an attribute.

            data = np.asarray(data, dtype='float32')

            setattr(self,
                    'data',
                    data)

            # Regular expression to parse keys
            # and values from a `BESTPROF` file.

            regex = re.compile(r'''
                               \#               # The comment char.
                               \s+              # Whitespace.
                               (?P<key>.+)      # The key.
                               =                # The separator char.
                               (?P<value>.+)    # The value.
                               ''', re.VERBOSE)

            for line in header:

                if re.search(regex, line):

                    # Get all keys and parameters.
                    # The `=` sign is the separator
                    # here. Use regular expressions
                    # to parse the file.

                    matches = re.search(regex,
                                        line)

                    mdict = matches.groupdict()

                    key   = mdict['key'].strip()
                    value = mdict['value'].strip()

                    if not key in BESTPROFKEYS:
                        continue
                    else:

                        [key,
                         ktype] = BESTPROFtoVARS[key]

                        # If value is N/A, exchange it
                        # for `None`. Otherwise, try a
                        # type conversion.

                        if value != 'N/A':
                            value = ktype(value)
                        else:
                            value = None

                        # Check if the value returned
                        # is in the form of a tuple.
                        # if yes, separate the quantity
                        # and it's error and store them
                        # as separate attributes. If not,
                        # just store the value as is.

                        if isinstance(value, tuple):

                            qty = value[0]
                            err = value[1]

                            qtykey = key
                            errkey = ''.join([key,
                                             'err'])


                            setattr(self,
                                    qtykey,
                                    float(qty))

                            setattr(self,
                                    errkey,
                                    float(err))

                        else:

                            setattr(self,
                                    key,
                                    value)
