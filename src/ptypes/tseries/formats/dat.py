import typing
import numpy as np  # type: ignore

from pathlib import Path
from ptypes.metadata import Metadata


def datread(f: str) -> typing.Tuple[Metadata, np.ndarray]:

    """"""

    inf = Path(f).with_suffix(".inf")

    if not inf.exists():
        msg = "No corresponding *.inf file found. Exiting..."
        raise OSError(msg)

    meta = Metadata.frominf(inf)

    with open(f, "rb") as fobj:
        data = np.fromfile(
            fobj,
            dtype="float32",
        )

    return meta, data


def datwrite(f: str) -> None:

    """"""

    pass
