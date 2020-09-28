import pprint


class PType(object):
    def __init__(self, fname: str):

        self.fname: str = fname

    def __str__(self) -> str:
        return "{}\n{}".format(self.__class__, pprint.pformat(self.__dict__))

    def __repr__(self) -> str:
        return str(self)
