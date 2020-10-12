import re
import typing
import numpy as np  # type: ignore

from schema import (  # type: ignore
    Or,
    Use,
    Schema,
)


def strex(val: typing.Any) -> typing.Any:
    val = str(val)
    if val == "N/A":
        return None
    else:
        return val


def numex(str: str) -> typing.Any:
    numex = re.compile(
        """
        [+-]                # Match a `+` or a `-`.
        ?                   # Match between 0 and 1 of the preceding token.
        (?:0|[1-9]\d*)      # Match a single 0, or any non-zero numeric value.
        (?:\.\d*)           # Match zero or more numeric values after a decimal point.
        ?                   # Match between 0 and 1 of the preceding token.
        (?:[eE][+\-]?\d+)   # Match one or more numeric values after an exponent
                            # (indicated by `e` or `E`). The values may be preceded
                            # by a `+` or `-` sign too.
        ?                   # Match between 0 and 1 of the preceding token.
        """,
        re.X,
    )
    nums = re.findall(numex, str)
    if nums:
        if len(nums) == 1:
            return nums[0]
        else:
            return nums
    else:
        return None


bprofmap = {
    "fname": strex,
    "candname": strex,
    "telescope": strex,
    "eptopo": numex,
    "epbary": numex,
    "tsamp": numex,
    "nsamp": numex,
    "davg": numex,
    "dstd": numex,
    "nbins": numex,
    "profavg": numex,
    "profstd": numex,
    "chisqr": numex,
    "nsigma": numex,
    "dm": numex,
    "ptopo": numex,
    "pdtopo": numex,
    "pddtopo": numex,
    "pbary": numex,
    "pdbary": numex,
    "pddbary": numex,
    "porb": numex,
    "asinc": numex,
    "eccen": numex,
    "wrad": numex,
    "tperi": numex,
}


bprofsch = Schema(
    {
        key: Or(
            None,
            Use(value),
        )
        for key, value in bprofmap.items()
    }
)


bproftemplate = (
    "# Input file       =  {fname}\n"
    "# Candidate        =  {candname}\n"
    "# Telescope        =  {telescope}\n"
    "# Epoch_topo       =  {eptopo}\n"
    "# Epoch_bary       =  {epbary}\n"
    "# T_sample         =  {tsamp}\n"
    "# Data Folded      =  {nsamp}\n"
    "# Data Avg         =  {davg}\n"
    "# Data StdDev      =  {dstd}\n"
    "# Profile Bins     =  {nbins}\n"
    "# Profile Avg      =  {profavg}\n"
    "# Profile StdDev   =  {profstd}\n"
    "# Reduced chi-sqr  =  {chisqr}\n"
    "# Prob(Noise)      <  0   (~{nsigma} sigma)\n"
    "# Best DM          =  {dm}\n"
    "# P_topo (ms)      =  {ptopo}\n"
    "# P'_topo (s/s)    =  {pdtopo}\n"
    "# P''_topo (s/s^2) =  {pddtopo}\n"
    "# P_bary (ms)      =  {pbary}\n"
    "# P'_bary (s/s)    =  {pdbary}\n"
    "# P''_bary (s/s^2) =  {pddbary}\n"
    "# P_orb (s)        =  {porb}\n"
    "# asin(i)/c (s)    =  {asinc}\n"
    "# eccentricity     =  {eccen}\n"
    "# w (rad)          =  {wrad}\n"
    "# T_peri           =  {tperi}\n"
    "######################################################\n"
)


errtemplate = "{value:16} +/- {error}"


def mclean(m: typing.Dict) -> typing.Dict:

    """"""

    d = {}

    for key, val in m.items():
        if isinstance(val, list):
            suffix = "_err"
            err = "".join([key, suffix])
            d[key] = val[0]
            d[err] = val[1]
        else:
            d[key] = val
    return d


def mdirty(m: typing.Dict) -> typing.Dict:

    """"""

    d = {}

    for key, value in m.items():

        if value:
            d[key] = value
        else:
            d[key] = "N/A"

        suffix = "_err"
        errkey = "".join([key, suffix])
        error = m.get(errkey, None)

        if error:
            d[key] = errtemplate.format(
                value=value,
                error=error,
            )

    return d


def bprofread(f: str) -> typing.Tuple:

    """"""

    m: typing.Dict[str, typing.Any] = {}

    metex = re.compile(r"^#.*", re.M)
    sepex = re.compile(r"\s+[=<>]\s+")
    numex = re.compile(r"\d+\.\d+")
    datex = re.compile(r"^\s+\d+\s+(.+)$", re.M)

    with open(f, "r") as fobj:
        lines = fobj.read()

    meta = re.findall(metex, lines)
    data = re.findall(datex, lines)

    meta = meta[:-1]

    keys = bprofmap.keys()
    values = [re.split(sepex, field)[-1] for field in meta]
    m = {key: value for (key, value) in zip(keys, values)}
    m = bprofsch.validate(m)
    m["nsigma"] = m["nsigma"][-1]
    m = mclean(m)

    d = np.asarray(data, dtype=np.float32)

    return m, d


def bprofwrite(
    m: typing.Dict,
    d: np.ndarray,
    f: str,
) -> None:

    """"""

    m = mdirty(m)

    text = bproftemplate.format(
        fname=m["fname"],
        candname=m["candname"],
        telescope=m["telescope"],
        eptopo=m["eptopo"],
        epbary=m["epbary"],
        tsamp=m["tsamp"],
        nsamp=m["nsamp"],
        davg=m["davg"],
        dstd=m["dstd"],
        nbins=m["nbins"],
        profavg=m["profavg"],
        profstd=m["profstd"],
        chisqr=m["chisqr"],
        nsigma=m["nsigma"],
        dm=m["dm"],
        ptopo=m["ptopo"],
        pdtopo=m["pdtopo"],
        pddtopo=m["pddtopo"],
        pbary=m["pbary"],
        pdbary=m["pdbary"],
        pddbary=m["pddbary"],
        porb=m["porb"],
        asinc=m["asinc"],
        eccen=m["eccen"],
        wrad=m["wrad"],
        tperi=m["tperi"],
    )

    with open(f, "w+") as fobj:
        fobj.write(text)
        for ind, point in enumerate(d):
            fobj.write(
                "{ind:>5}  {point}\n".format(
                    ind=ind,
                    point=point,
                )
            )
