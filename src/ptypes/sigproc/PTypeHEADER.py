import struct

from pathlib import Path

from ptypes import PType
from ptypes.consts.misc    import *
from ptypes.consts.sigproc import *


DEFAULT = 'Unknown'


class PTypeHEADER(PType):

    """
    Class to handle the reading of `SIGPROC` style
    headers from various `SIGPROC` binary formats,
    such as `FIL`, `TIM`, and `SPEC` files.

    Used with most `PTypes` defined in this module.
    """

    def __init__(self,
                 fname):

        """
        Create an instance of `PTypeHEADER`.
        """

        super().__init__(fname)

        self.read()

    def __readAttr__(self,
                     fobj,
                     keys):

        """
        Private function to read a single attribute
        from a `SIGPROC` style header.

        Inputs:

        fobj: File object.

            An open File object attached to the file from
            which the binary values of the header need to
            be read.

        keys: list

            A list of all possible keys for a `SIGPROC` style
            header. If the key being read is not a part of the
            list, an error is raised.
        """

        # Read the format character and size
        # needed to unpack the keys from the
        # `SIGPROC` style header. All keys are
        # of type `int`.

        (ctype,
         csize) = FORMATCHARS['int']

        # Read in the buffer and calculate
        # the number of bytes we need to
        # read to unpack the key string.

        buffer   = fobj.read(csize)
        bufsize, = struct.unpack(ctype, buffer)

        # Unpack and decode the key string.

        key = str(fobj.read(bufsize).decode())

        # If key is the `ENDFLAG`, return and exit.

        if key == ENDFLAG:
            return key, None

        # Get the type for the value associated
        # with the key being read. If the type
        # does not exist, will return a default
        # value of `None`.

        btype = keys.get(key, None)

        # If `None` is returned as the type,
        # cannot read the value associated
        # with the key. Raise an error and
        # exit.

        if not btype:
            ERROR = ('Type of SIGPROC header '
                     'attribute \'{0:s}\' is '
                     'unknown, please specify it.')

            ERROR = ERROR.format(key)

            raise KeyError(ERROR)

        # If the type is `str`, need to unpack
        # and decode these bytes in the same way
        # as the key.

        if btype == 'str':

            (ctype,
             csize) = FORMATCHARS['int']

            buffer   = fobj.read(csize)
            bufsize, = struct.unpack(ctype,
                                     buffer)

            value = fobj.read(bufsize)
            value = value.decode()

        # If the type is `int` or `double`, can
        # directly unpack the bytes. Get the
        # format character and size, and unpack
        # accordingly.

        elif any([btype == 'int',
                  btype == 'double']):

            (ctype,
             csize) = FORMATCHARS[btype]

            buffer = fobj.read(csize)
            value, = struct.unpack(ctype,
                                   buffer)

        # Cannot read this key. Raise error
        # and exit.

        else:

            ERROR = ('Key \'{0:s}\' has unsupported'
                     'type \'{1:s}\'. Cannot read it.')

            ERROR = ERROR.format(key,
                                 btype)

            raise ValueError(ERROR)

        # If all goes well, return the
        # (key, value) pair.

        return key, value

    def read(self):

        """
        Read a `SIGPROC` style header into an
        instance of `PTypeHEADER`. The start
        and end of the header are indicated by
        flags (`STARTFLAG` and `ENDFLAG`). If
        those flags are absent, we cannot read
        the header from the file.
        """

        # This is a list of all possible keys
        # in a `SIGPROC` style header. We are
        # renaming the variable for readability.

        keys = SIGPROCKEYS

        # Open the file in binary mode.

        with open(self.fname, 'rb') as infile:

            # Get format character and size for
            # the start and end flags. They are
            # of type `int`.

            (ctype,
             csize) = FORMATCHARS['int']

            # If not already there, set the seek
            # to the beginning of the file because
            # that's where the header is.

            infile.seek(0)

            # Read the buffer in and get the
            # size of the string to be read.

            buffer   = infile.read(csize)
            bufsize, = struct.unpack(ctype,
                                     buffer)

            # Unpack and decode the string. If
            # the flag is not the same as the
            # `STARTFLAG`, raise an error and
            # exit immediately.

            FLAG  = str(infile.read(bufsize).decode())
            ERROR = ('File starts with \'{0:s}\' '
                     'flag instead of the expected '
                     '\'{1:s}\'.')

            ERROR = ERROR.format(FLAG,
                                 STARTFLAG)

            if not (FLAG == STARTFLAG):
                raise ValueError(ERROR)

            # Start reading in the header. If
            # we reach the `ENDFLAG`, break the
            # loop. Set all attributes.

            while True:

                (key,
                 value) = self.__readAttr__(infile,
                                            keys)

                if key == ENDFLAG:
                    break

                setattr(self,
                        key,
                        value)

            # Set some additional parameters, such
            # as header size, telescope and machine
            # name, data type etc.

            self.hdrsize = infile.tell()

            IDMACH = IDtoMACHINE
            IDTELE = IDtoTELESCOPE
            DTYPES = DATATYPES

            self.telescope = IDTELE.get(self.telescope_id, DEFAULT)
            self.machine   = IDMACH.get(self.machine_id, DEFAULT)
            self.dtype     = DTYPES.get(self.data_type, DEFAULT)

    def write(self,
              fname):

        """
        """

        keys = SIGPROCKEYS

        with open(fname, 'wb+') as infile:

            fsize = struct.pack('i', len(STARTFLAG))
            fstrg = STARTFLAG.encode()

            infile.write(fsize)
            infile.write(fstrg)

            for key in keys:

                (ctype,
                 csize) = FORMATCHARS['int']

                try:
                    value = getattr(self, key)
                    print(key, value)
                except AttributeError:
                    continue

                ktype = type(value)
                ksize = struct.pack(ctype, len(key))
                kstrg = key.encode()

                infile.write(ksize)
                infile.write(kstrg)

                if ktype == str:

                    (ctype,
                     csize) = FORMATCHARS['int']

                    vsize = struct.pack(ctype, len(value))
                    vstrg = value.encode()

                    infile.write(vsize)
                    infile.write(vstrg)

                elif ktype == int:

                    (ctype,
                     csize) = FORMATCHARS['int']

                    vbytes = struct.pack(ctype, value)

                    infile.write(vbytes)

                elif ktype == float:

                    (ctype,
                     csize) = FORMATCHARS['double']

                    vbytes = struct.pack(ctype, value)

                    infile.write(vbytes)

            fsize = struct.pack('i', len(ENDFLAG))
            fstrg = ENDFLAG.encode()

            infile.write(fsize)
            infile.write(fstrg)
