import typing
import numpy as np  # type: ignore

from pathlib import Path
from ptypes.metadata import Metadata


bits2dtypes = {
    1: "<u1",
    2: "<u1",
    4: "<u1",
    8: "<u1",
    16: "<u2",
    32: "<f4",
}


def timread(f: str) -> typing.Tuple[Metadata, np.ndarray]:

    """"""

    meta = Metadata.fromhdr(f)

    with open(f, "rb") as fobj:
        fobj.seek(meta.size)
        nbits = meta.nbits
        dtype = bits2dtypes[nbits]

        data = np.fromfile(
            f,
            dtype=dtype,
        )

        data = data.astype("float32")

    return meta, data


def timwrite(f: str) -> None:

    """"""

    pass
