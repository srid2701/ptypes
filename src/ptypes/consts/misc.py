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
