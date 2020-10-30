import re
import typing

from construct import (  # type: ignore
    GreedyRange,
    PaddedString,
)


keycon = GreedyRange(PaddedString(80, "utf8"))

typemap = {
    str: re.compile(r"^\'(?P<val>.+)\'$"),
    int: re.compile(r"^(?P<val>\d*)$"),
    float: re.compile(r"^(?P<val>\d*\.\d*)$"),
}


def mgupread(
    f: typing.Any,
) -> typing.Dict[str, typing.Any,]:

    """"""

    d: typing.Dict[str, typing.Any] = {}

    if isinstance(f, str):
        pairs = keycon.parse_file(f)
    else:
        pairs = keycon.parse_stream(f)

    pairs = pairs[:-1]
    pairs = [pair.split("=") for pair in pairs]
    for pair in pairs:
        key = pair[0].strip()
        val = pair[1].strip()
        for vtype, vrex in typemap.items():
            match = re.search(vrex, val)
            if match:
                val = match.groupdict()["val"]
                val = vtype(val)
                d[key] = val
                break
    return d


def mgupwrite(
    d: typing.Dict[str, typing.Any],
    f: typing.Any,
) -> None:

    """"""

    pass
