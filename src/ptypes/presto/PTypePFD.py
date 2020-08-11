import struct
import numpy as np

from pathlib import Path

from ptypes.consts.misc   import *
from ptypes.consts.presto import *
from ptypes.consts.phymath import *
from ptypes.core.basis import PType

from .PTypeINF import PTypeINF
from .PTypeBESTPROF import PTypeBESTPROF


def doppler(OBSFREQ,
            VOVERC):

    """
    This routine returns the frequency emitted by a
    pulsar (in MHz) given that we observe the pulsar
    at frequency `OBSFREQ` (MHz) while moving with a
    radial velocity (in units of v/c) of `VOVERC` with
    respect to the pulsar.
    """

    FACTOR    = (1.0 + VOVERC)
    SHIFTFREQ = OBSFREQ * FACTOR

    return SHIFTFREQ

def delays(DM,
           EMITFREQ):

    """
    Return the delay in seconds caused by dispersion,
    given a Dispersion Measure (`DM`) in cm-3 pc, and
    the emitted frequency (`EMITFREQ`) of the pulsar in
    MHz.
    """

    FACTOR = 0.000241

    if type(EMITFREQ) is float:
        if EMITFREQ > 0.0:

            DELAY = (DM
                     / (FACTOR
                        * (EMITFREQ ** 2)))

            return DELAY

        else:

            DELAY = 0.0
            return DELAY

    else:

        DELAY = (DM
                 / (FACTOR
                    * (EMITFREQ ** 2)))

        return np.where(EMITFREQ > 0.0,
                        DELAY,
                        0.0)

def FFTrotate(array,
              nbins):

    """
    Return 'array' rotated by 'nbins' places to the
    left. The rotation is done in the Fourier domain
    using the `Shift Theorem`. The value of 'nbins'
    can be fractional.

    Input(s):

    array: list or numpy.array

        An array of numbers representing a vector.

    nbins: int or float

        The number of bins by which the array should
        be rotated to the left. This value can be a
        fractional one as well.

    Output(s):

    sarray: numpy.array

        The resulting array, with bins shifted to the
        left by `nbins`. It has the same length as the
        original array.
    """

    array = np.asarray(array)
    freqs = np.arange(array.size / 2 + 1,
                      dtype=np.float)

    iTWOPI = complex(0.0, TWOPI)
    phasor = np.exp(iTWOPI
                    * freqs
                    * bins
                    / float(array.size))

    sarray = np.fft.irfft((phasor
                           * np.fft.rfft(array)),
                          array.size)

    return sarray

class PTypePFD(PType):

    BPROFEXT   = '.bestprof'
    POLYCOSEXT = '.polycos'

    RALEN  = 16
    DECLEN = 16

    """
    Class to handle `PFD` (PRESTO Folded Data) files.
    This stores three-dimensional folded data in a
    binary format.

    This code is a cleaned-up version of the code of the
    `pfd` class written by Scott Ransom in the Python code
    packaged in the newest release (v3.0.1) of `PRESTO`.
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

    def _writeValues_(self,
                      fobj,
                      values,
                      btype='int'):

        """
        """

        (ctype,
         csize) = FORMATCHARS[btype]

        cstring = ctype * len(values)
        packets = struct.pack(cstring, *values)

        fobj.write(packets)

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

    def _writeString_(self,
                      fobj,
                      string,
                      btype='int'):

        """
        """

        (ctype,
         csize) = FORMATCHARS[btype]

        strsize = len(string)
        binsize = struct.pack(ctype, strsize)
        string  = string.encode('utf-8')

        fobj.write(binsize)
        fobj.write(string)

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

    def _writeArray_(self,
                     fobj,
                     array,
                     btype='double'):

        """
        """

        (ctype,
         csize) = FORMATCHARS[btype]

        cstring = ctype * len(array)
        packets = struct.pack(cstring, *array)

        fobj.write(packets)

    def _setAttrs_(self,
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

    def _getAttrs_(self,
                   keys):

        """
        """

        values = []

        for key in keys:
            value = getattr(self, key)
            values.append(value)

        return values

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
            self._setAttrs_(keys, values)

            # Stop! Have to process strings differently.
            # Reading:
            #
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
            # the first `RALEN` bytes of the file and
            # test if the coordinates are in a proper
            # format for reading or not, and if there
            # are any coordinates at all. Coordinates
            # might be absent from the file, or simply
            # `Unknown`.

            test = infile.read(self.RALEN)

            if not test[:8]==b"Unknown" and b':' in test:

                self.rastr = test[:test.find(b'\0')]
                self.rastr = self.rastr.decode('utf-8')

                test = infile.read(self.DECLEN)

                self.decstr = test[:test.find(b'\0')]
                self.decstr = self.decstr.decode('utf-8')
            else:
                self.rastr  = "Unknown"
                self.decstr = "Unknown"

                if ':' not in test:
                    infile.seek(-self.RALEN, 1)

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

            self._setAttrs_(keys, values)

            # Stop!

            (ctype,
             csize) = FORMATCHARS['float']

            bufsize = csize * 2
            buffer  = infile.read(bufsize)

            (self.topopow,
             self._ttmp_) = struct.unpack(ctype * 2,
                                          buffer)

            keys = ['topop1',
                    'topop2',
                    'topop3']

            values = self._readValues_(infile,
                                       len(keys),
                                       btype='double')

            self._setAttrs_(keys, values)

            # Stop!

            buffer  = infile.read(bufsize)

            (self.barypow,
             self._btmp_) = struct.unpack(ctype * 2,
                                          buffer)

            keys = ['baryp1',
                    'baryp2',
                    'baryp3']

            values = self._readValues_(infile,
                                       len(keys),
                                       btype='double')

            self._setAttrs_(keys, values)

            # Stop!

            buffer  = infile.read(bufsize)

            (self.foldpow,
             self._ftmp_) = struct.unpack(ctype * 2,
                                          buffer)

            keys = ['foldp1',
                    'foldp2',
                    'foldp3']

            values = self._readValues_(infile,
                                       len(keys),
                                       btype='double')

            self._setAttrs_(keys, values)

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

            self._setAttrs_(keys, values)

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

            # If there is only 1 DM value, store it
            # as a single variables rather than as a
            # list.

            if self.numdms == 1:
                self.dms = self.dms[0]

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

            # If the number of frequency channels
            # is one, then that implies that the
            # folded data is from the folding of
            # a dedispersed time series. We should
            # thus take the relevant data from the
            # corresponding `INF` file, if present.

            if self.numchan == 1:

                try:

                    infname = Path(self.fname).with_suffix(INFEXT)
                    infdata = PTypeINF(infname)

                    try:
                        if infdata.obstype == 'Radio':
                            self.bestdm  = infdata.dm
                            self.numchan = infdata.nchan
                    except:
                        self.bestdm  = 0.0
                        self.numchan = 1

                except IOError:

                    ERRMSG = ('Warning! '
                              'Cannot open the '
                              '{:s} file '
                              'for {:s}')
                    ERRMSG.format(INFEXT, self.fname)

                    print(ERRMSG)

            # Time to calculate and store some
            # other parameters before we go on
            # with reading the file. These are:
            #
            #

            self.secBINS   = self.foldp1 * self.proflen
            self.subCHANS  = self.numchan // self.nsub
            self.subDFREQ  = self.chanwidth * self.subCHANS

            self.hifreq = (self.lofreq
                           + (self.numchan
                              * self.chanwidth)
                           - self.chanwidth)

            self.subLFREQ = (self.lofreq
                             + self.subDFREQ
                             - self.chanwidth)

            self.subFREQS = (np.arange(self.nsub,
                                       dtype='d')
                             * self.subDFREQ
                             + self.subLFREQ)

            self.subDBINS = np.zeros(self.nsub, dtype='d')

            self.currDM = 0.0

            self.killSUBBANDS  = []
            self.killINTERVALS = []
            self.pointsPERFOLD = []

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

                # Append `numdata` from `foldstats`
                # to the points per fold. This is
                # the first value in a `foldstats`
                # object.

                self.pointsPERFOLD.append(self.stats[pindx][0][0])

            self.pointsPERFOLD = np.asarray(self.pointsPERFOLD)

        self.startSECS = ((np
                           .add
                           .accumulate([0,
                                        *self.pointsPERFOLD[:-1]]))
                          * self.tsamp)

        print(self.tsamp)
        print(self.startSECS.shape)
        print(self.pointsPERFOLD.shape)

        self.midSECS = self.startSECS + (0.5
                                         * self.tsamp
                                         * self.pointsPERFOLD)

        if self.tepoch != 0.0:

            self.startTOPOMJDS = (self.startSECS
                                  / SECPERDAY) + self.tepoch

            self.midTOPOMJDS = (self.midSECS
                                / SECPERDAY) + self.tepoch

        if self.bepoch != 0.0:

            self.startBARYMJDS = (self.startSECS
                                  / SECPERDAY) + self.bepoch

            self.midBARYMJDS = (self.midSECS
                                / SECPERDAY) + self.bepoch

        self.numfold  = np.add.reduce(self.pointsPERFOLD)
        self.numsamp  = self.numfold * self.tsamp
        self.avgprof  = (self.profs / self.proflen).sum()
        #self.varprof = self._calcVarProf_()

        #self.DOFnom = float(self.proflen) - 1.0
        #self.DOFcor = self.DOFnom * self.DOFCORRECTION

        self.subBARYFREQS = None
        """
        if self.avgoverc == 0:

            if self.candname.startswith(PSRSUFFIX):

                try:

                    POLYFILE = self.fname.with_suffix(POLYCOSEXT)
                    self.polycos = (PTypePOLYCOS(fname=POLYFILE))

                    midMJD = self.tepoch + (0.5
                                            * self.numsamp
                                            / SECPERDAY)

                    self.avgoverc = (self
                                     .polycos
                                     .getvoverc(int(mindMJD),
                                                (midMJD
                                                 - int(midMJD))))

                    self.subBARYFREQS = (self.subFREQS
                                         * (1.0
                                            + self.avgoverc))

                except IOError:

                    self.polycos = 0

            if self.subBARYFREQS is None:

                self.subBARYFREQS = self.subFREQS
        """
    def write(self,
              fname):

        """
        Write an instance of `PTypePFD` into a `PFD` file.
        """

        with open(fname, 'wb+') as infile:

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

            values = self._getAttrs_(keys)
            self._writeValues_(infile, values)

            keys = ['filename',
                    'candname',
                    'telescope',
                    'pgdev']

            for key in keys:
                string = getattr(self, key)
                self._writeString_(infile, string)

            try:

                pad = b'\x00'

                if not ((self.rastr == "Unknown")
                        and
                        (self.decstr == "Unknown")):

                    rabinary = self.rastr.encode('utf-8')
                    numpad   = (self.RALEN - len(rabinary))
                    padding  = pad * numpad
                    rabinary = b''.join([rabinary, padding])

                    decbinary = self.decstr.encode('utf-8')
                    numpad    = (self.DECLEN - len(decbinary))
                    padding   = pad * numpad
                    decbinary  = b''.join([decbinary, padding])

                else:

                    rabinary  = b'Unknown'
                    decbinary = b'Unknown'

                infile.write(rabinary)
                infile.write(decbinary)

            except AttributeError:
                pass

            keys = ['tsamp',
                    'startT',
                    'endT',
                    'tepoch',
                    'bepoch',
                    'avgoverc',
                    'lofreq',
                    'chanwidth',
                    'bestdm']

            values = self._getAttrs_(keys)

            self._writeValues_(infile,
                               values,
                               btype='double')

            (ctype,
             csize) = FORMATCHARS['float']

            topopow = struct.pack(ctype * 2,
                                  self.topopow,
                                  self._ttmp_)

            infile.write(topopow)

            keys = ['topop1',
                    'topop2',
                    'topop3']

            values = self._getAttrs_(keys)

            self._writeValues_(infile,
                               values,
                               btype='double')

            barypow = struct.pack(ctype * 2,
                                  self.barypow,
                                  self._btmp_)

            infile.write(barypow)

            keys = ['baryp1',
                    'baryp2',
                    'baryp3']

            values = self._getAttrs_(keys)

            self._writeValues_(infile,
                               values,
                               btype='double')

            foldpow = struct.pack(ctype * 2,
                                  self.foldpow,
                                  self._ftmp_)

            infile.write(foldpow)

            keys = ['foldp1',
                    'foldp2',
                    'foldp3']

            values = self._getAttrs_(keys)

            self._writeValues_(infile,
                               values,
                               btype='double')

            keys = ['orbp',
                    'orde',
                    'ordx',
                    'ordw',
                    'orbt',
                    'ordpd',
                    'ordwd']

            values = self._getAttrs_(keys)

            self._writeValues_(infile,
                               values,
                               btype='double')

            arrays = ['dms',
                      'periods',
                      'pdots']

            for name in arrays:
                array = getattr(self, name)
                self._writeArray_(infile, array)

            pindxs = range(self.npart)
            sindxs = range(self.nsub)

            for pindx in pindxs:
                for sindx in sindxs:

                    profile = self.profs[pindx,
                                         sindx,
                                         :].tobytes()

                    infile.write(profile)

            for pindx in pindxs:
                cstats = self.stats[pindx]
                for sindx in sindxs:

                    statarr = cstats[sindx].tobytes()
                    infile.write(statarr)

    def dedisperse(self,
                   DM=None,
                   INTERP=False,
                   DOPPLER=False):

        """
        """

        if DM is None:
            DM = self.bestdm

        # NOTE: Since `TEMPO` Doppler corrects
        # observing frequencies, for TOAs, at
        # least, we need to de-disperse using
        # topocentric observing frequencies.

        if DOPPLER:
            FREQS = doppler(self.subFREQS,
                            self.avgoverc)
        else:
            FREQS = self.subFREQS

        subDELAYS = delays(DM, FREQS)
        subDELAYS = (subDELAYS - subDELAYS[-1])

        delayBINS =  (subDELAYS
                      * self.secBINS
                      - self.subDBINS)

        if INTERP:

            subDBINS = delayBINS

            pindxs = range(self.npart)
            sindxs = range(self.nsub)

            for pindx in pindxs:
                for sindx in sindx:

                    temprof = self.profs[pindx,
                                         sindx,
                                         :]

                    self.profs[pindx,
                               sindx] = FFTrotate(temprof,
                                                  delayBINS[sindx])

            # NOTE: Since the rotation process we just did
            # slightly changes the values of the profiles,
            # we need to re-calculate the average profile
            # value.

            self.avgprof = (self.profs / self.proflen).sum()

        else:

            subDBINS = np.floor(delayBINS + 0.5)

            pindxs = range(self.npart)
            sindxs = range(self.nsub)

            for sindx in sindxs:

                rotBINS = (int(subDBINS[sindx])
                           % self.proflen)

                if rotBINS != 0:

                    subDATA = self.profs[:,
                                         sindx,
                                         :]

                    subTUPLE = (subDATA[:,rotBINS:],
                                subDATA[:,:rotBINS])

                    self.profs[:,
                               sindx] = np.concatenate(subTUPLE, 1)

        self.subDBINS = self.subDBINS + subDBINS
        self.sumPROF  = self.profs.sum(0).sum(0)

        profCHECK = (self.sumPROF / self.proflen).sum() - self.avgprof

        if np.fabs(profCHECK > 1.0):
            ERRMSG = ('Average profile does not '
                      'have the correct value.  ')

            print(ERRMSG)

        self.currDM = DM
