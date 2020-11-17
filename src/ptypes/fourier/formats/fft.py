import numpy as np  # type: ignore

from pathlib import Path
from typing import Tuple, Optional
from ptypes.metadata import Metadata


def fftread(f: str) -> Tuple[Metadata, np.ndarray]:

    """"""

    inf = Path(f).with_suffix(".inf")

    if not inf.exists():
        msg = "No corresponding *.inf file found. Exiting..."
        raise OSError(msg)

    meta = Metadata.frominf(str(inf))

    with open(f, "rb") as fobj:
        data = np.fromfile(
            fobj,
            dtype="float32",
        )

    return meta, data


def fftwrite(
    data: np.ndarray,
    meta: Metadata,
    f: Optional[str] = None,
) -> None:

    """"""

    inf = meta["fname"]

    if not f:
        f = str(Path(inf).with_suffix(".dat"))

    meta.toinf(str(inf))

    with open(f, "wb+") as fobj:
        data.tofile(fobj)
