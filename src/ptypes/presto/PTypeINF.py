import re

from pathlib import Path

from ptypes.consts.presto import *
from ptypes.core.basis import PType

class PTypeINF(PType):

    """
    Class to handle `INF` files, which store additional
    information about the time series data stored in a
    `DAT` file. These files are human-readable, but this
    class is required to parse the variables.

    This class is used with class `PTypeDAT`.
    """

    def __init__(self, fname):

        """
        Create an instance of `PTypeINF`.
        """

        super().__init__(fname)

        self.read()

    def read(self):

        """
        Read an `INF` file into an instance of `PTypeINF`.
        """

        INFKEYS = INFtoVARS.keys()
        INFKEYS = list(INFKEYS)

        # Regular expression to parse keys
        # and values from an INF file.

        regex = re.compile(r'''
                           (?P<key>.+)      # The key.
                           =                # The separator.
                           (?P<value>.+)    # The value.
                           ''', re.VERBOSE)

        with open(self.fname, 'r') as lines:

            # Initialise empty list to store
            # the additional notes at the end
            # of the file.

            notes = []

            for line in lines:

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

                    if not key in INFKEYS:
                        continue
                    else:

                        [key,
                         ktype] = INFtoVARS[key]

                        setattr(self,
                                key,
                                ktype(value))

                else:

                    # Append additional notes.

                    notes.append(line)

            # Clip the heading from additional notes
            # at the end of the INF file, and then
            # store them in the `notes` attribute.

            notes = notes[1:]
            notes = [note.strip()
                     for note in notes]
            notes = [note
                     for note in notes
                     if note]

            setattr(self,
                    'notes',
                    notes)
