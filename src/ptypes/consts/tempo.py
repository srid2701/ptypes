DEFSPAN = 60
DEFNUMCOEFF = 12

TELESCOPEtoID = {
    "GBT": "1",
    "Arecibo": " 3",
    "VLA": "6",
    "Parkes": "7",
    "Jodrell": "8",
    "GB43m": "a",
    "GB 140FT": "a",
    "Nancay": "f",
    "Effelsberg": "g",
    "WSRT": "i",
    "FAST": "k",
    "GMRT": "r",
    "CHIME": "y",
    "Geocenter": "0",
    "Barycenter": "@",
}

IDtoTELESCOPE = {}

IDtoTELESCOPE = dict(zip(TELESCOPEtoID.values(), TELESCOPEtoID.keys()))

TELESCOPEtoMAXHA = {
    "GBT": 12,
    "Arecibo": 3,
    "FAST": 5,
    "VLA": 6,
    "Parkes": 12,
    "Jodrell": 12,
    "GB43m": 12,
    "GB 140FT": 12,
    "Nancay": 4,
    "Effelsberg": 12,
    "WSRT": 12,
    "GMRT": 12,
    "CHIME": 1,
    "Geocenter": 12,
    "Barycenter": 12,
}
