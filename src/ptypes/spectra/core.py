import numpy as np

class Spectra(object):

    def __init__(self,
                 freqs,
                 tsamp,
                 data,
                 DM=0.0,
                 startT=0.0,
                 endT=1.0):

        """
        """

        self.data = data.astype('float')

        [self.numchans,
         self.numspecs] = self.data.shape

        if len(freqs) != self.numchans:

            ERRMSG = ('Number of observing frequencies '
                      'does not correspond to number of '
                      'channels in the data.')

            raise ValueError(ERRMSG)

        self.freqs  = freqs
        self.tsamp  = tsamp

        self.DM     = DM
        self.startT = startT
        self.endT   = endT

    def __str__(self):
        return str(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def getchan(self, channum):
        return self.data[channum,:]

    def getspec(self, specnum):
        return self.data[:,specnum]

    def shiftchans(self,
                   bins,
                   padval=0):

        """
        """

        cindxs = range(self.numchans)

        for cindx in cindxs:

            channel    = self.getchan(cindx)
            channel[:] = rotate(channel,
                                bins[cindx])

            if padval is not 'rotate':
                if padval is 'mean':
                    padding = np.mean(channel)
                elif padval is 'median':
                    padding = np.median(channel)
                else:
                    padding = padval

                if bins[cindx] > 0:
                    channel[-bins[cindx]:] = padding
                elif bins[cindx] < 0:
                    channel[:-bins[cindx]] = padding

    def subband(self,
                nsub,
                padval=0,
                subDM=None):

        """
        """

        if (self.numchans % nsub) != 0:

            ERRMSG = ('Number of subbands is not '
                      'a factor of the number of '
                      'channels. Cannot do subbanding!')

            raise ValueError(ERRMSG)

        DM    = self.dm
        TSAMP = self.tsamp

        NSUBs = np.arange(nsub)
        FREQs = self.freqs
        RELDM = subDM - DM

        subCHANs   = self.numchans // nsub
        subHIFREQs = self.freqs[NSUBs * subCHANs]
        subLOFREQs = self.freqs[((1 + NSUBs)
                                 * subCHANs
                                  - 1)]

        subCFREQs = 0.5 * (subHIFREQs + subLOFREQs)

        if subdm is not None:
            if subdm < 0:
                ERRMSG = ('DM cannot be less than zero.')
                raise ValueError(ERRMSG)
            else:

                refDELs    = delays(RELDM, subCFREQs)
                absDELs    = delays(RELDM, FREQs)
                relDELs    = (absDELs - refDELs.repeat(subCHANs))
                relBINDELs = np.round(relDELs/TSAMP).astype('int')

                self.shiftchans(relBINDELs, padval)

        SPLITs = np.vsplit(self.data, nsub)

        SUMs   = [np.sum(SPLIT, axis=0)
                  for SPLIT in SPLITs]

        self.data    = np.array(SUMs)
        self.freqs   = subCFREQs
        self.numchans = nsub
