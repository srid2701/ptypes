import re
import typing


def str2bool(string: str) -> bool:

    """
    Convert string to boolean.
    """

    return int(string) != 0


def bool2str(boolean: bool) -> str:

    """
    Convert boolean to string.
    """

    if boolean:
        string = "1"
    else:
        string = "0"
    return string


infmap = [
    ("bsname", str),
    ("telescope", str),
    ("instrument", str),
    ("source", str),
    ("raj", str),
    ("decj", str),
    ("observer", str),
    ("mjd", float),
    ("barycentered", str2bool),
    ("nsamp", int),
    ("tsamp", float),
    ("breaks", str2bool),
    ("obstype", str),
    ("fov", float),
    ("dm", float),
    ("fbot", float),
    ("bandwidth", float),
    ("nchan", int),
    ("cbw", float),
    ("analyst", str),
    ("notes", str),
]

inftemplate = (
    " Data file name without suffix          =  {bsname}\n"
    " Telescope used                         =  {telescope}\n"
    " Instrument used                        =  {instrument}\n"
    " Object being observed                  =  {source}\n"
    " J2000 Right Ascension (hh:mm:ss.ssss)  =  {raj}\n"
    " J2000 Declination     (dd:mm:ss.ssss)  =  {decj}\n"
    " Data observed by                       =  {observer}\n"
    " Epoch of observation (MJD)             =  {mjd:.15f}\n"
    " Barycentered?           (1 yes, 0 no)  =  {barycentered}\n"
    " Number of bins in the time series      =  {nsamp}\n"
    " Width of each time series bin (sec)    =  {tsamp}\n"
    " Any breaks in the data? (1 yes, 0 no)  =  {breaks}\n"
    " Type of observation (EM band)          =  {obstype}\n"
    " Beam diameter (arcsec)                 =  {fov}\n"
    " Dispersion measure (cm-3 pc)           =  {dm}\n"
    " Central freq of low channel (MHz)      =  {fbot}\n"
    " Total bandwidth (MHz)                  =  {bandwidth}\n"
    " Number of channels                     =  {nchan}\n"
    " Channel bandwidth (MHz)                =  {cbw}\n"
    " Data analyzed by                       =  {analyst}\n"
    " Any additional notes:\n"
    "    {notes}"
)


def infread(f: str) -> typing.Dict[str, typing.Any]:

    """"""

    d = {}

    d["fname"] = f

    with open(f, "r") as fobj:
        text = fobj.read()
        text = text.strip()

    lines = re.split("\n+", text)
    regex = re.compile(r"(?P<descr>.+)=(?P<value>.+)")

    extralines = []

    for indx, line in enumerate(lines):

        match = re.search(regex, line)

        if match:
            mamap = match.groupdict()
            descr = mamap["descr"].strip()
            value = mamap["value"].strip()
            (kname, ktype) = infmap[indx]
            d[kname] = ktype(value)  # type: ignore
        else:
            extralines.append(line)

    d["notes"] = "\n".join(extralines[1:]).strip()

    return d


def infwrite(
    d: typing.Dict[str, typing.Any],
    f: typing.Optional[str] = None,
) -> None:

    """"""

    if not f:
        bsname = d["bsname"]
        default = "".join([bsname, ".inf"])
        fname = d.get("fname", default)
    else:
        fname = f

    text = inftemplate.format(
        bsname=d["bsname"],
        telescope=d["telescope"],
        instrument=d["instrument"],
        source=d["source"],
        raj=d["raj"],
        decj=d["decj"],
        observer=d["observer"],
        mjd=d["mjd"],
        barycentered=bool2str(d["barycentered"]),
        nsamp=d["nsamp"],
        tsamp=d["tsamp"],
        breaks=bool2str(d["breaks"]),
        obstype=d["obstype"],
        fov=d["fov"],
        dm=d["dm"],
        fbot=d["fbot"],
        bandwidth=d["bandwidth"],
        nchan=d["nchan"],
        cbw=d["cbw"],
        analyst=d["analyst"],
        notes=d["notes"],
    )

    with open(fname, "w+") as fobj:
        fobj.write(text)
