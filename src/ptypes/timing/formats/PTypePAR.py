from ptypes import PType

ERRKW = "_ERR"


class PTypePAR(PType):

    """"""

    def __init__(self, fname):

        """
        Create a `PTypePAR` instance.
        """

        super().__init__(fname)

        self.read()
        self.clean()
        self.procs()

    def read(self):

        """
        Read a `PAR` file into an instance of `PTypePAR`.
        """

        with open(str(self.fname), "r") as lines:

            # Iterate through all the lines
            # in the `PAR` file.

            for line in lines:

                # Split each line using whitespace
                # as the separator. We only want to
                # split the line once, so we set the
                # `maxsplit` parameter to `1`.

                cuts = line.split(maxsplit=1)

                # Check if `cuts` is not an empty list.

                if cuts:

                    # Get (key, value) pair.

                    [key, values] = cuts

                    # Split value. This helps
                    # us get the error, if it
                    # is present.

                    values = values.split()

                    setattr(self, key, values[0])

                    # Check if there is an error
                    # value present or not, by
                    # checking the length of the
                    # split list.

                    if len(values) > 1:

                        # Use separate key for
                        # errors. This is just
                        # the original key with
                        # a `ERR` keyword attached
                        # at the end.

                        err = "".join([key, ERRKW])

                        setattr(self, err, values[-1])

    def clean(self):

        """
        Clean all data we just read in through the
        `read` function, by doing all appropriate
        type conversions. Except for a few values,
        most are either ints or floats.
        """

        # These keys are not to be disturbed
        # since they were always meant to be
        # strings.

        STRKEYS = ["fname", "PSRJ", "NAME", "SURVEY", "OSURVEY", "UNITS"]

        # Iterate through all attributes.

        for key, value in self.__dict__.items():

            # If the key is not meant
            # to be a string, convert
            # it into an appropriate
            # type.

            if key not in STRKEYS:

                # If the value has a colon
                # in it, it is a coordinate
                # value. Let it remain as a
                # string.

                if value.find(":") != -1:
                    pass

                # If the value has a decimal
                # in it, convert it to float.

                elif value.find(".") != -1:
                    value = float(value)

                # If all else fails, it is must
                # be an integer. Type convert it
                # to int.

                else:
                    value = int(value)

                # Reset the attribute.

                setattr(self, key, value)

    def procs(self):

        """
        Process some of the values we just read in
        and cleaned. We mostly have to:

        1. Process the coordinates appropriately.
        2. Calculate and store missing variables.
        """

        pass
