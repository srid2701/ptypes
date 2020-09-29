from construct import (  # type: ignore
    Int8ul,
    Int8ub,
    Int32ul,
    Int32ub,
    Float32l,
    Float32b,
    Float64l,
    Float64b,
    PascalString,
)

TELESCOPEtoID = {
    "Fake": 0,
    "Arecibo": 1,
    "ARECIBO 305m": 1,
    "Ooty": 2,
    "Nancay": 3,
    "Parkes": 4,
    "Jodrell": 5,
    "GBT": 6,
    "GMRT": 7,
    "Effelsberg": 8,
    "ATA": 9,
    "SRT": 10,
    "LOFAR": 11,
    "VLA": 12,
    "CHIME": 20,
    "FAST": 21,
    "MeerKAT": 64,
    "KAT-7": 65,
}

IDtoTELESCOPE = {}

IDtoTELESCOPE = dict(zip(TELESCOPEtoID.values(), TELESCOPEtoID.keys()))

MACHINEtoID = {
    "FAKE": 0,
    "PSPM": 1,
    "Wapp": 2,
    "WAPP": 2,
    "AOFTM": 3,
    "BCPM1": 4,
    "BPP": 4,
    "OOTY": 5,
    "SCAMP": 6,
    "GBT Pulsar Spigot": 7,
    "SPIGOT": 7,
    "BG/P": 11,
    "PDEV": 12,
    "CHIME+PSR": 20,
    "KAT": 64,
    "KAT-DC2": 65,
}

IDtoMACHINE = dict(zip(MACHINEtoID.values(), MACHINEtoID.keys()))

DATATYPES = {
    1: "Filterbank file",
    2: "Timeseries file",
}

SIGPROCKEYS = {
    "filename": PascalString(Int32ul, "utf8"),
    "telescope_id": Int32ul,
    "telescope": PascalString(Int32ul, "utf8"),
    "machine_id": Int32ul,
    "data_type": Int32ul,
    "rawdatafile": PascalString(Int32ul, "utf8"),
    "source_name": PascalString(Int32ul, "utf8"),
    "barycentric": Int32ul,
    "pulsarcentric": Int32ul,
    "az_start": Float64l,
    "za_start": Float64l,
    "src_raj": Float64l,
    "src_dej": Float64l,
    "tstart": Float64l,
    "tsamp": Float64l,
    "nbits": Int32ul,
    "nsamples": Int32ul,
    "fch1": Float64l,
    "foff": Float64l,
    "fchannel": Float64l,
    "nchans": Int32ul,
    "nifs": Int32ul,
    "refdm": Float64l,
    "flux": Float64l,
    "period": Float64l,
    "nbeams": Int32ul,
    "ibeam": Int32ul,
    "hdrlen": Int32ul,
    "pb": Float64l,
    "ecc": Float64l,
    "asini": Float64l,
    "orig_hdrlen": Int32ul,
    "new_hdrlen": Int32ul,
    "sampsize": Int32ul,
    "bandwidth": Float64l,
    "fbottom": Float64l,
    "ftop": Float64l,
    "obs_date": PascalString(Int32ul, "utf8"),
    "obs_time": PascalString(Int32ul, "utf8"),
    "signed": Int8ul,
    "accel": Float64l,
}

STARTFLAG = "HEADER_START"
ENDFLAG = "HEADER_END"
