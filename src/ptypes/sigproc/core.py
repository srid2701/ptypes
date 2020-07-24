import re
import struct
import numpy as np

from pathlib import Path

from ptypes import PType
from ptypes.consts import *

class PTypeHEADER(PType):

    """
    """

    def __init__(self,
                 fname):

        """
        """

        super().__init__(fname)

        self.read()

    def __readAttr__(self,
                     fobj,
                     keys):

        """
        """

        (ctype,
         csize) = FORMATCHARS['int']

        buffer   = fobj.read(csize)
        bufsize, = struct.unpack(ctype, buffer)

        key = str(fobj.read(bufsize).decode())

        if key == ENDFLAG:
            return key, None

        btype = keys.get(key, None)

        if not btype:
            ERROR = ('Type of SIGPROC header '
                     'attribute \'{0:s}\' is '
                     'unknown, please specify it.')

            ERROR = ERROR.format(key)

            raise KeyError(ERROR)

        if btype == 'str':

            (ctype,
             csize) = FORMATCHARS['int']

            buffer   = fobj.read(csize)
            bufsize, = struct.unpack(ctype,
                                    buffer)

            value = fobj.read(bufsize)
            value = value.decode()

        elif any([btype == 'int',
                  btype == 'double']):

            (ctype,
             csize) = FORMATCHARS[btype]

            buffer = fobj.read(csize)
            value, = struct.unpack(ctype,
                                   buffer)
        else:

            ERROR = ('Key \'{0:s}\' has unsupported'
                     'type \'{1:s}\'. Cannot read it.')

            ERROR = ERROR.format(key,
                                 btype)

        return key, value

    def read(self):

        """
        """

        keys = SIGPROCKEYS

        with open(self.fname, 'rb') as infile:

            (ctype,
             csize) = FORMATCHARS['int']

            infile.seek(0)

            buffer   = infile.read(csize)
            bufsize, = struct.unpack(ctype,
                                     buffer)

            FLAG  = str(infile.read(bufsize).decode())
            ERROR = ('File starts with \'{0:s}\' '
                     'flag instead of the expected '
                     '\'{1:s}\'.')

            ERROR = ERROR.format(FLAG,
                                 STARTFLAG)

            if not (FLAG == STARTFLAG):
                raise ValueError(ERROR)

            while True:

                (key,
                 value) = self.__readAttr__(infile,
                                            keys)

                if key == ENDFLAG:
                    break

                setattr(self,
                        key,
                        value)

            self.hdrsize = infile.tell()

            IDs            = IDtoTELESCOPE['SIGPROC']

            self.telescope = IDs.get(self.telescope_id,
                                     'Unknown')

            self.machine   = IDtoMACHINE.get(self.machine_id,
                                             'Unknown')

            self.data_type = DATATYPES.get(self.data_type,
                                           'Unknown')


class PTypeTIM(PType):

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


class PTypeRAW(PType):

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
