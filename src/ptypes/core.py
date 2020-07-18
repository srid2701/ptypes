class PType(object):

    def __init__(self,
                 fname,
                 nbits):

        self.nbits = nbits
        self.fname = fname

    def read(self):
        raise NotImplementedError

    def write(self):
        raise NotImplementedError
