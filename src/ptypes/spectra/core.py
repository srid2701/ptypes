import copy
import numpy as np
import scipy.signal

from ptypes.utils import delays

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

        self.data     = np.array(SUMs)
        self.freqs    = subCFREQs
        self.numchans = nsub

    def meanscl(self,
                indep=False):

        """
        """

        CLONE = copy.deepcopy(self)

        if not indep:
            std = CLONE.data.std()

        cindxs = range(self.numchans)

        for cindx in cindxs:

            channel = other,getchan(cindx)

            median = np.median(channel)

            if indep:
                std = channel.std()

            channel[:] = (channel - median)/std


    def minmax(self,
               indep=False):

        """
        """

        CLONE = copy.deepcopy(self)

        if not indep:
            maxima = CLONE.data.max()

        cindxs = range(self.numchans)

        for cindx in cindxs:

            channel = other,getchan(cindx)

            minima = channel.min()

            if indep:
                maxima = channel.max()

            channel[:] = (channel - minima)/maxima

    def masked(self,
               mask,
               value=0,
               method='mid80'):

        """
        """

        if mask.shape != self.data.shape:

            ERRMSG = ('The dimensions of the mask do '
                      'not match the dimensions of the '
                      'spectra data.')

            raise ValueError(ERRMSG)

        values = np.ones(self.numchans)
        cindxs = range(self.numchans)

        for cindx in cindxs:

            channel = self.getchan(cindx)

            if method is 'mean':
                values[cindx] = np.mean(channel)
            elif method is 'median':
                values[cindx] = np.medain(channel)
            elif method is 'mid80':

                num = int(np.round(0.1
                                   * self.numspecs))

                values = np.median(sorted(channel)[num:-num])
            else:
                values[cindx] = value

            if np.all(mask[cindx]):
                self.data[cindx] = (np.ones_like(self.data[cindx])
                                    * (values[:,
                                              np.newaxis][cindx]))

            return self

    def dedisperse(self,
                   DM=0,
                   PAD=0):

        """
        """

        if DM < 0:
            ERRMSG = ('DM cannot be less than zero!')
            raise ValueError(ERRMSG)

        refDEL     = delays(DM - self.dm, np.max(self.freqs))
        DELs       = delays(self.dm, self.freqs)
        relDELs    = (DELs - refDEL)
        relBINDELs = np.round(relDELs/self.tsamp).astype('int')

        self.shiftchans(relBINDELs, PAD)

        self.dm = DM

    def smooth(self,
               width=1,
               padval=0,
               padmethod=None):

        """
        """

        if width > 1:

            kernel = np.ones(width,
                             dtpye='float32') / np.sqrt(width)

            cindxs = range(self.numchans)

            for cindx in cindxs:

                channel = getchan(cindx)

                if padmethod is not None:

                    if padmethod is 'wrap':

                        tosmooth = np.concatenate([channel[-width:],
                                                   channel,
                                                   channel[:width]])

                    elif padmethod is 'mean':

                        tosmooth = np.ones(self.numspecs
                                           + width
                                           * 2) * np.mean(channel)

                    elif padmethod is 'median':

                        tosmooth = np.ones(self.numspecs
                                           + width
                                           * 2) * np.median(channel)

                else:

                    tosmooth = np.ones(self.numspecs
                                       + width
                                       * 2) / padval

                    tosmooth[width:-width] = channels

                smoothed = (scipy
                            .signal
                            .convolve(tosmooth,
                                      kernel,
                                      'same'))

                channel[:] = smoothed[width:-width]

    def trim(self,
             bins=0):

        """
        """

        if bins > self.numspecs:

            ERRMSG = ('Bins to trim more than '
                      'number of spectra in the '
                      'data. Cannot trim!')

            raise ValueError(ERRMSG)

        if bins is 0:
            return
        elif bins > 0:
            self.data     = self.data[:,:-bins]
            self.numspecs = self.numspecs - bins
        elif bins < 0:
            self.data = self.data[:,bins:]
            self.numspecs = self.numspecs - bins
            self.startT = (self.startT
                           + bins
                           * self.tsamp)

    def downsamp(self,
                 factor=1,
                 trime=True):

        """
        """

        if not trim:
            if not self.numspecs % factor:

                ERRMSG = ('Downsampling factor not a factor'
                          ' of the number of spectra in the'
                          ' data. Cannot downsample.')

                raise ValueError(ERRMSG)

        numspecs = self.numspecs // factor
        numtrim  = self.numspecs %  factor

        self.trim(numtrim)

        subints    = np.hsplit(self.data, numspecs)
        summations = [np.sum(subint, axis=1)
                      for subint in subints]
        colstack   = np.column_stack(summations)

        self.data     = np.array(colstack)
        self.numspecs = numspecs
        self.tsamp    = self.tsamp * factor
