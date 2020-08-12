from ptypes import PType

class PTypePAR(PType):

    """
    """

    ERRKW = '_ERR'

    def __init__(self,
                 fname):

        """
        Create a `PTypePAR` instance.
        """

        super().__init__(fname)

        self.read()
        self.process()

    def read(self):

        """
        Read a `PAR` file into an instance of `PTypePAR`.
        """

        with open(self.fname, 'r') as lines:

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

                    [key,
                     values] = cuts

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

                        err = ''.join([key,
                                       self.ERRKW])

                        setattr(self, err, values[-1])

    def process(self):

        """
        Process all values read into a `PTypePAR` instance.
        This does all the relevant type conversions for all
        variables we just stored through the `read` function.
        """

        # These keys are not to be disturbed
        # since they were always meant to be
        # strings.

        STRKEYS = ['fname',
                   'PSRJ',
                   'NAME',
                   'SURVEY',
                   'UNITS']

        # Iterate through all attributes.

        for key, value in (self
                           .__dict__
                           .items()):

            # If the key is not meant
            # to be a string, convert
            # it into an appropriate
            # type.

            if key not in STRKEYS:

                # If the value has a colon
                # in it, it is a coordinate
                # value. Let it remain as a
                # string.

                if value.find(':') != -1:
                    pass

                # If the value has a decimal
                # in it, convert it to float.

                elif value.find('.') != -1:
                    value = float(value)

                # If all else fails, it is must
                # be an integer. Type convert it
                # to int.

                else:
                    value = int(value)

                # Reset the attribute.

                setattr(self,
                        key,
                        value)
