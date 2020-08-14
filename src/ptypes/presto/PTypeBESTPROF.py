import re
import numpy as np

from pathlib import Path

from ptypes import PType
from ptypes.consts.presto import *


class PTypeBESTPROF(PType):

    """
    Class to handle `BESTPROF` files, which store the
    best profile of a particular candidate folded using
    `PRESTO`. These files are human-readable, but this
    class is required to parse the variables.

    This class is used with class 'PTypePFD'.
    """

    def __init__(self, fname):

        """
        Create an instance of `PTypeBESTPROF`.
        """

        super().__init__(fname)

        self.read()

    def read(self):

        """
        Read an `BESTPROF` file into an instance
        of `PTypeBESTPROF`.
        """

        BESTPROFKEYS = BPROFtoVARS.keys()
        BESTPROFKEYS = list(BESTPROFKEYS)

        with open(self.fname, 'r') as infile:

            lines = infile.read()

            # Regular expression to separate header
            # and data in a `BESTPROF` file.

            regex = re.compile(r'\#{2,}')

            # Separate header and data.

            [header,
             data] = re.split(regex, lines)

            # Split header and data along
            # newline characters.

            header = re.split(r'\n+', header)
            data   = re.split(r'\n+', data)

            for indx, line in enumerate(data):

                number = line.strip()
                point  = re.split(r'\s+',
                                  number)[-1]
                data[indx] = point

            # Remove empties from data.

            data = [number
                    for number in data
                    if number]

            # Type convert data to a `numpy`
            # array and store it in this class
            # as an attribute.

            data = np.asarray(data, dtype='float32')

            setattr(self,
                    'data',
                    data)

            # Regular expression to parse keys
            # and values from a `BESTPROF` file.

            regex = re.compile(r'''
                               \#               # The comment char.
                               \s+              # Whitespace.
                               (?P<key>.+)      # The key.
                               =                # The separator char.
                               (?P<value>.+)    # The value.
                               ''', re.VERBOSE)

            for line in header:

                if re.search(regex, line):

                    # Get all keys and parameters.
                    # The `=` sign is the separator
                    # here. Use regular expressions
                    # to parse the file.

                    matches = re.search(regex,
                                        line)

                    mdict = matches.groupdict()

                    key   = mdict['key'].strip()
                    value = mdict['value'].strip()

                    if not key in BESTPROFKEYS:
                        continue
                    else:

                        [key,
                         ktype] = BPROFtoVARS[key]

                        # If value is N/A, exchange it
                        # for `None`. Otherwise, try a
                        # type conversion.

                        if value != 'N/A':
                            value = ktype(value)
                        else:
                            value = None

                        # Check if the value returned
                        # is in the form of a tuple.
                        # if yes, separate the quantity
                        # and it's error and store them
                        # as separate attributes. If not,
                        # just store the value as is.

                        if isinstance(value, tuple):

                            qty = value[0]
                            err = value[1]

                            qtykey = key
                            errkey = ''.join([key,
                                             'err'])


                            setattr(self,
                                    qtykey,
                                    float(qty))

                            setattr(self,
                                    errkey,
                                    float(err))

                        else:

                            setattr(self,
                                    key,
                                    value)
