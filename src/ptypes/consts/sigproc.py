TELESCOPEtoID = {
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
}

IDtoTELESCOPE = {}

IDtoTELESCOPE = dict(
                     zip(
                         TELESCOPEtoID.values(),
                         TELESCOPEtoID.keys()
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
