import re

FORMATCHARS = {
    'pad': ('x', None),
    'bool': ('?', 1),
    'char': ('c', 1),
    'signed_char': ('b', 1),
    'unsigned_char': ('B', 1),
    'short': ('h', 2),
    'unsigned_short': ('H', 2),
    'int': ('i', 4),
    'unsigned_int': ('I', 4),
    'long': ('l', 4),
    'unsigned long': ('L', 4),
    'long_long': ('q', 8),
    'unsigned_long_long': ('Q', 8),
    'float': ('f', 4),
    'double': ('d', 8),
}

NBITStoDTYPE = {
    1: '<u1',
    2: '<u1',
    4: '<u1',
    8: '<u1',
    16: '<u2',
    32: '<f4',
}

def strOfBool(str):
    """
    Convert string to boolean.
    """
    return int(str) != 0

INFtoVARS = {
    'Data file name without suffix': ['basename', str],
    'Telescope used': ['telescopeID', str],
    'Instrument used': ['machineID', str],
    'Object being observed': ['srcname', str],
    'J2000 Right Ascension (hh:mm:ss.ssss)': ['srcRA', str],
    'J2000 Declination     (dd:mm:ss.ssss)': ['srcDEC', str],
    'Epoch of observation (MJD)': ['mjd', float],
    'Barycentered?           (1 yes, 0 no)': ['barycentric', strOfBool],
    'Number of bins in the time series': ['nbins', int],
    'Width of each time series bin (sec)': ['tsamp', float],
    'Any breaks in the data? (1 yes, 0 no)': ['break', strOfBool],
    'Type of observation (EM band)': ['obstype', str],
    'Beam diameter (arcsec)': ['beamdiam', float],
    'Dispersion measure (cm-3 pc)': ['dm', float],
    'Central freq of low channel (MHz)': ['cfreq', float],
    'Total bandwidth (MHz)': ['bw', float],
    'Number of channels': ['nchan', int],
    'Channel bandwidth (MHz)': ['chanbw', float],
    'Data analyzed by': ['analyst', str],
}

def getError(string):

    """
    Separate quantity and error from
    a string representing them. Meant
    to be used for decoding BESTPROF
    files.
    """

    regex = re.compile(r'\+/-')

    [qty,
     err] = re.split(regex, string)

    return qty, err

BESTPROFtoVARS = {
    'Input file': ['fname', str],
    'Candidate': ['candname', str],
    'Telescope': ['telescope', str],
    'Epoch_topo': ['eptopo', float],
    'Epoch_bary': ['epbary', float],
    'T_sample': ['tsamp', float],
    'Data Folded': ['nsamp', float],
    'Data Avg': ['davg', float],
    'Data StdDev': ['dstd', float],
    'Profile Bins': ['nbins', int],
    'Profile Avg': ['profavg', float],
    'Profile StdDev': ['profstd', float],
    'Reduced chi-sqr': ['chisqr', float],
    'Best DM': ['dm', float],
    'P_topo (ms)': ['ptopo', getError],
    'P\'_topo (s/s)': ['pdtopo', getError],
    'P\'\'_topo (s/s^2)': ['pddtopo', getError],
    'P_bary (ms)': ['pbary', getError],
    'P\'_bary (s/s)': ['pdbary', getError],
    'P\'\'_bary (s/s^2)': ['pddbary', getError],
    'P_orb (s)': ['porb', float],
    'asin(i)/c (s)': ['asinc', float],
    'eccentricity': ['eccen', float],
    'w (rad)': ['wrad', float],
    'T_peri': ['tperi', float],
}

TELESCOPEtoID = {

    'SIGPROC': {
        'Fake': 0,
        'Arecibo': 1,
        'ARECIBO 305m': 1,
        'Ooty': 2,
        'Nancay': 3,
        'Parkes': 4,
        'Jodrell': 5,
        'GBT': 6,
        'GMRT': 7,
        'Effelsberg': 8,
        'ATA': 9,
        'SRT': 10,
        'LOFAR': 11,
        'VLA': 12,
        'CHIME': 20,
        'FAST': 21,
        'MeerKAT': 64,
        'KAT-7': 65,
    },

    'TEMPO': {
        'GBT': '1',
        'Arecibo':' 3',
        'VLA': '6',
        'Parkes': '7',
        'Jodrell': '8',
        'GB43m': 'a',
        'GB 140FT': 'a',
        'Nancay': 'f',
        'Effelsberg': 'g',
        'WSRT': 'i',
        'FAST': 'k',
        'GMRT': 'r',
        'CHIME': 'y',
        'Geocenter': '0',
        'Barycenter': '@',
    }
}

IDtoTELESCOPE = {}

for key, value in TELESCOPEtoID.items():

    IDtoTELESCOPE[key] = dict(
                             zip(
                                 value.values(),
                                 value.keys()
                                )
                             )

MACHINEtoID = {
    'FAKE': 0,
    'PSPM': 1,
    'Wapp': 2,
    'WAPP': 2,
    'AOFTM': 3,
    'BCPM1': 4,
    'BPP': 4,
    'OOTY': 5,
    'SCAMP': 6,
    'GBT Pulsar Spigot': 7,
    'SPIGOT': 7,
    'BG/P': 11,
    'PDEV': 12,
    'CHIME+PSR': 20,
    'KAT': 64,
    'KAT-DC2': 65,}

IDtoMACHINE = dict(
                  zip(
                      MACHINEtoID.values(),
                      MACHINEtoID.keys()
                     )
                  )

DATATYPES = {
    1: 'Filterbank file',
    2: 'Timeseries file',
}

TELESCOPEtoMAXHA = {
    'GBT': 12,
    'Arecibo': 3,
    'FAST': 5,
    'VLA': 6,
    'Parkes': 12,
    'Jodrell': 12,
    'GB43m': 12,
    'GB 140FT': 12,
    'Nancay': 4,
    'Effelsberg': 12,
    'WSRT': 12,
    'GMRT': 12,
    'CHIME': 1,
    'Geocenter': 12,
    'Barycenter': 12,
}

SIGPROCKEYS = {
    'filename': 'str',
    'telescope_id': 'int',
    'telescope': 'str',
    'machine_id': 'int',
    'data_type': 'int',
    'rawdatafile': 'str',
    'source_name': 'str',
    'barycentric': 'int',
    'pulsarcentric': 'int',
    'az_start': 'double',
    'za_start': 'double',
    'src_raj': 'double',
    'src_dej': 'double',
    'tstart': 'double',
    'tsamp': 'double',
    'nbits': 'int',
    'nsamples': 'int',
    'fch1': 'double',
    'foff': 'double',
    'fchannel': 'double',
    'nchans': 'int',
    'nifs': 'int',
    'refdm': 'double',
    'flux': 'double',
    'period': 'double',
    'nbeams': 'int',
    'ibeam': 'int',
    'hdrlen': 'int',
    'pb':'double',
    'ecc':'double',
    'asini':'double',
    'orig_hdrlen': 'int',
    'new_hdrlen': 'int',
    'sampsize': 'int',
    'bandwidth': 'double',
    'fbottom': 'double',
    'ftop': 'double',
    'obs_date': 'str',
    'obs_time': 'str',
    'signed': 'signed_char',
    'accel': 'double',
}

STARTFLAG = 'HEADER_START'
ENDFLAG   = 'HEADER_END'


PSRFITSKEYS = {
    'PRIMARY': [
        'FITSTYPE',
        'TELESCOP',
        'OBSERVER',
        'SRC_NAME',
        'FRONTEND',
        'BACKEND',
        'PROJID',
        'DATE-OBS',
        'FD_POLN',
        'RA',
        'DEC',
        'OBSFREQ',
        'OBSNCHAN',
        'OBSBW',
        'BMIN',
        'CHAN_DM',
        'STT_IMJD',
        'STT_SMJD',
        'STT_OFFS',
        'STT_LST',
        'TRK_MODE'
    ],

    'SUBINT': [
        'TBIN',
        'NCHAN',
        'NPOL',
        'POL_TYPE',
        'NCHNOFFS',
        'NSBLK',
        'NBITS',
        'NAXIS2',
        'NSUBOFFS',
        'ZERO_OFF',
    ],

    'SUBINT-HDU': [
        'OFFS_SUB',
        'DATA',
        'TEL_AZ',
        'TEL_ZEN',
        'DAT_FREQ',
        'DAT_WTS',
        'DAT_OFFS',
        'DAT_SCL',
    ]
}

PSRFITSTEMP = [
    'From the PSRFITS file {:s}:',
    '                       HDUs = {:s}',
    '                  Telescope = {:s}',
    '                   Observer = {:s}',
    '                Source Name = {:s}',
    '                   Frontend = {:s}',
    '                    Backend = {:s}',
    '                 Project ID = {:s}',
    '            Obs Date String = {:s}',
    '  MJD start time (DATE-OBS) = {:5d.14s}',
    '     MJD start time (STT_*) = {:19.14',
    '                   RA J2000 = {:s}',
    '             RA J2000 (deg) = {:-17.15g',
    '                  Dec J2000 = {:s}',
    '            Dec J2000 (deg) = {:-17.15g}',
    '                  Tracking? = {:s}',
    '              Azimuth (deg) = {:-.7g}',
    '           Zenith Ang (deg) = {:-.7g}',
    '          Polarisation type = {:s}',
    '            Number of polns = {:s}',
    '         Polarisation order = {:s}',
    '           Sample time (us) = {:-17.15g}',
    '         Central freq (MHz) = {:-17.15g}',
    '          Low channel (MHz) = {:-17.15g}',
    '   Orig Channel width (MHz) = {:-17.15g}',
    '    Orig Number of channels = {:d}',
    '    DM used for chan dedisp = {:-17.15g}',
    '      Total Bandwidth (MHz) = {:-17.15g}',
    '         Spectra per subint = {:d}',
    '            Starting subint = {:d}',
    '           Subints per file = {:d}',
    '           Spectra per file = {:d}',
    '        Time per file (sec) = {:-.12g}',
    '              FITS typecode = {:s}',
    '                DATA column = {:d}',
    '            Bits per sample = {:d}',
    '          Bytes per spectra = {:d}',
    '        Samples per spectra = {:d}',
    '           Bytes per subint = {:d}',
    '         Samples per subint = {:d}',
    '              Need scaling? = {:s}',
    '              Need offsets? = {:s}',
    '              Need weights? = {:s}',
    '        Need band inverted? = {:s}',
]
