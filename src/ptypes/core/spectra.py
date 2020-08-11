class Spectra(object):

    def __init__(self,
                 freqs,
                 tsamp,
                 data,
                 DM=0,
                 startT=0,
                 endT=1):

        """
        """

        self.data = data.astype('float')

        [self.numchan,
         self.numspec] = self.data.shape

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

    def get_chan(self, channum):
        return self.data[channum,:]

    def get_spec(self, specnum):
        return self.data[:,specnum]
