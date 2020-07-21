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

TELESCOPEtoID = {'GBT': '1',
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
                 'Barycenter': '@'}

IDtoTELESCOPE = dict(
                    zip(
                        TELESCOPEtoID.values(),
                        TELESCOPEtoID.keys()
                        )
                    )

TELESCOPEtoMAXHA = {'GBT': 12,
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
                    'Barycenter': 12}
