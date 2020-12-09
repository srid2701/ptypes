import attr
import numpy as np  # type: ignore

from pathlib import Path
from ptypes.metadata import NoMeta, Metadata
from .formats import fftread, fftwrite, specread, specwrite
from typing import Any, Type, List, Dict, Tuple, TypeVar, Optional


F = TypeVar("F", bound="Fourier")


@attr.s(auto_attribs=True)
class Fourier(object):

    """"""

    data: np.ndarray

    nsamp: int
    tsamp: float

    freq: np.ndarray
    phas: np.ndarray
    pows: np.ndarray

    meta: Optional[Metadata] = None

    @classmethod
    def fromnpy(
        cls: Type[F],
        d: np.ndarray,
        nsamp: int,
        tsamp: float,
        meta: Optional[Metadata] = None,
    ) -> F:

        """"""

        freq = np.fft.fftfreq(nsamp, tsamp)
        phas = np.angle(d)
        pows = np.abs(d) ** 2

        return cls(
            d,
            nsamp=nsamp,
            tsamp=tsamp,
            freq=freq,
            phas=phas,
            pows=pows,
            meta=meta,
        )

    @classmethod
    def fromfft(
        cls: Type[F],
        f: str,
    ) -> F:

        """"""

        meta, data = fftread(f)
        nsamp = meta["nsamp"]
        tsamp = meta["tsamp"]
        return cls.fromnpy(
            data,
            nsamp=nsamp,
            tsamp=tsamp,
            meta=meta,
        )

    @classmethod
    def fromspec(
        cls: Type[F],
        f: str,
    ) -> F:

        """"""

        meta, data = specread(f)
        nsamp = meta["nsamp"]
        tsamp = meta["tsamp"]
        return cls.fromnpy(
            data,
            nsamp=nsamp,
            tsamp=tsamp,
            meta=meta,
        )

    def tonpy(self) -> np.ndarray:

        """"""

        return self.data

    def tofft(
        self,
        f: str,
    ) -> None:

        """"""

        if self.meta:
            fftwrite(
                self.data,
                self.meta,
                f,
            )

    def tospec(
        self,
        f: str,
    ) -> None:

        """"""

        if self.meta:
            specwrite(
                self.data,
                self.meta,
                f,
            )
        else:
            raise NoMeta(
                """
                Metadata absent.
                Cannot write to a *.tim file.
                Exiting...
                """
            )
