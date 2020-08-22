import numpy as np

from ptypes.consts import TWOPI

def doppler(OBSFREQ,
            VOVERC):

    """
    This routine returns the frequency emitted by a
    pulsar (in MHz) given that we observe the pulsar
    at frequency `OBSFREQ` (MHz) while moving with a
    radial velocity (in units of v/c) of `VOVERC` with
    respect to the pulsar.
    """

    FACTOR    = (1.0 + VOVERC)
    SHIFTFREQ = OBSFREQ * FACTOR

    return SHIFTFREQ

def delays(DM,
           EMITFREQ):

    """
    Return the delay in seconds caused by dispersion,
    given a Dispersion Measure (`DM`) in cm-3 pc, and
    the emitted frequency (`EMITFREQ`) of the pulsar in
    MHz.
    """

    FACTOR = 0.000241

    if type(EMITFREQ) is float:
        if EMITFREQ > 0.0:

            DELAY = (DM
                     / (FACTOR
                        * (EMITFREQ ** 2)))

            return DELAY

        else:

            DELAY = 0.0
            return DELAY

    else:

        DELAY = (DM
                 / (FACTOR
                    * (EMITFREQ ** 2)))

        return np.where(EMITFREQ > 0.0,
                        DELAY,
                        0.0)

def FFTrotate(array,
              nbins):

    """
    Return 'array' rotated by 'nbins' places to the
    left. The rotation is done in the Fourier domain
    using the `Shift Theorem`. The value of 'nbins'
    can be fractional.

    Input(s):

    array: list or numpy.array

        An array of numbers representing a vector.

    nbins: int or float

        The number of bins by which the array should
        be rotated to the left. This value can be a
        fractional one as well.

    Output(s):

    sarray: numpy.array

        The resulting array, with bins shifted to the
        left by `nbins`. It has the same length as the
        original array.
    """

    array = np.asarray(array)
    freqs = np.arange(array.size / 2 + 1,
                      dtype=np.float)

    iTWOPI = complex(0.0, TWOPI)
    phasor = np.exp(iTWOPI
                    * freqs
                    * nbins
                    / float(array.size))

    sarray = np.fft.irfft((phasor
                           * np.fft.rfft(array)),
                          array.size)

    return sarray
