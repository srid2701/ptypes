import struct
import numpy as np


class PTypeRESIDUAL(PType):

    """"""

    def __init__(self, fname):

        """"""

        super().__init__(fname)

        self.read()

    def read(self):

        """"""

        with open(str(self.fname), "rb") as infile:

            # Long hack to fix endianness and type of
            # data (long long or int). This hack just
            # checks if the data read has values that
            # are either too high, or negative. If so,
            # the data has been read with either the
            # wrong endianess, or with an incorrectly
            # specified data type.

            TBUF = 8
            RLEN = 9
            SWAP = "<"

            data = infile.read(TBUF)

            INT = FORMATCHARS["int"]
            LLG = FORMATCHARS["long_long"]

            ITYPE = "".join([SWAP, INT[0]])
            LTYPE = "".join([SWAP, LLG[0]])

            INT64 = struct.unpack(ITYPE, data)[0]
            INT32 = struct.unpack(LTYPE, data)[:4][0]

            TINT64 = INT64 > 100 or INT64 < 0
            TINT32 = INT32 > 100 or INT32 < 0

            if not TINT32:
                MTYPE = INT
                reclen = TINT32 + 2 * INT[1]
            elif not TINT64:
                MTYPE = LLG
                reclen = TINT64 + 2 * LLG[1]
            else:
                SWAP = ">"

            FTYPE = FORMATCHARS["double"]

            rectype = "".join([SWAP, MTYPE, RLEN * FTYPE[0], MTYPE])

            # Seek to the end of file
            # to find the size of the
            # file and then come back
            # to the beginning.

            infile.seek(0, 2)
            filelen = infile.tell()
            infile.seek(0, 0)

            # Initialise a few arrays.

            self.numTOAs = filelen // reclen
            self.baryTOA = np.zeros(self.numTOAs, "d")
            self.postfitphs = np.zeros(self.numTOAs, "d")
            self.postfitsec = np.zeros(self.numTOAs, "d")
            self.orbitphs = np.zeros(self.numTOAs, "d")
            self.baryfreq = np.zeros(self.numTOAs, "d")
            self.weight = np.zeros(self.numTOAs, "d")
            self.uncertainty = np.zeros(self.numTOAs, "d")
            self.prefitphs = np.zeros(self.numTOAs, "d")

            # Start reading residuals.

            for numTOA in self.numTOAs:

                buffer = infile.read(reclen)

                record = struct.unpack(rectype, buffer)

                (
                    self.baryTOA,
                    self.postfitphs,
                    self.postfitsec,
                    self.orbitphs,
                    self.baryfreq,
                    self.weight,
                    self.uncertainty,
                    self.prefitphs,
                ) = record[:8]

        if not np.nonzero(self.weight):
            del self.weight
        if not np.nonzero(self.orbitphs):
            del self.orbitphs
        if not np.nonzero(self.baryfreq):
            del self.baryfreq

        self.prefitsec = self.postfitsec / self.postfitphs * self.prefitphs

        self.uncertainty = self.uncertainty * 1.0e-6
