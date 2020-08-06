import pytest
import numpy as np

from pathlib import Path

from ptypes.consts import *
from ptypes.presto import (PTypeINF,
                           PTypeDAT,
                           PTypeFFT,
                           PTypePFD,
                           PTypeACCEL,
                           PTypeBESTPROF)

TESTDIR = Path(__file__).parent.resolve()
DATADIR = Path.joinpath(TESTDIR, 'data')

INFTEST   = Path.joinpath(DATADIR, 'test.inf')
DATTEST   = Path.joinpath(DATADIR, 'test.dat')
FFTTEST   = Path.joinpath(DATADIR, 'test.fft')
PFDTEST   = Path.joinpath(DATADIR, 'test.pfd')
BPROFTEST = Path.joinpath(DATADIR, 'test.pfd.bestprof')

INFVALS = [
    'fake_noise.4096ch.8bit.J2144-3933_DC1-de-dispersed_DM3.35',
    'GMRT',
    'Unknown',
    'J2144-3933',
    '21:44:00.0000',
    '-39:33:00.0000',
    '58017.604258730985748',
    '1',
    '3600000',
    '0.00016384',
    '0',
    'Radio',
    '3600',
    '3.35',
    '300.024926',
    '199.999488',
    '4096',
    '0.048828',
    'guest',
    [
        'Project ID unset, Date: 2017-09-21T14:23:32.5098.',
        '2 polns were summed.  Samples have 8 bits.'
    ],
]

def test_inf():

    inf = PTypeINF(INFTEST)

    # Run all assertions for `PTypeINF`
    # object. The values should be the
    # same as given in `INFVALS`. Type
    # conversion is done as per the types
    # in `INFtoVARS`.

    for (key,
         value) in zip(INFtoVARS.values(),
                       INFVALS):

        aname = key[0]
        atype = key[1]

        attrb = getattr(inf, aname)

        assert attrb == atype(value)

def test_dat():

    dat = PTypeDAT(DATTEST,
                   inf=INFTEST)

    # Run the same tests as run for
    # a `PTypeINF` object, because
    # they share the same attributes.

    for (key,
         value) in zip(INFtoVARS.values(),
                       INFVALS):

        aname = key[0]
        atype = key[1]

        attrb = getattr(dat, aname)

        assert attrb == atype(value)

    # Some extra assertions that need
    # to be tested for a `PTypeDAT`
    # object.

    assert dat.inf        == str(INFTEST)
    assert dat.bsname     == 'test'
    assert dat.fname      == str(DATTEST)
    assert dat.nsamples   == int(3600000)
    assert dat.data.size  == int(3600000)
    assert type(dat.data) == np.ndarray

def test_fft(): pass

def test_pfd(): pass

def test_bprof(): pass    
