import pprint

class PType(object):

    def __init__(self,
                 fname):
        
        self.fname = fname

    def __str__(self):
        return '{}\n{}'.format(self.__class__,
                               pprint.pformat(self.__dict__)
                               )

    def __repr__(self):
        return str(self)
