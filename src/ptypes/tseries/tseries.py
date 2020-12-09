import attr
import copy
import numpy as np  # type: ignore

from pathlib import Path
from ptypes.metadata import NoMeta, Metadata
from .formats import datread, datwrite, timread, timwrite
from typing import Any, Type, List, Dict, Tuple, TypeVar, Optional
from pkernels import dsamp, fold, fastrmed, generate  # type: ignore


T = TypeVar("T", bound="TimeSeries")


@attr.s(auto_attribs=True)
class TimeSeries(object):

    """"""

    data: np.ndarray
    tsamp: float
    meta: Metadata = Metadata({})
    _copy: bool = False

    def copy(self: T) -> T:

        """"""

        return copy.deepcopy(self)

    def normalise(
        self: T,
        inplace: bool = False,
    ) -> Any:

        """"""

        v = self.data.var(dtype=np.float64)
        m = self.data.mean(dtype=np.float64)

        norm = v ** 0.5

        if inplace:
            self.data = (self.data - m) / norm
            return None
        else:
            return TimeSeries(
                (self.data - m) / norm,
                tsamp=self.tsamp,
                meta=self.meta,
            )

    def deredden(
        self: T,
        width: float,
        minpts: int = 10,
        inplace: bool = False,
    ) -> Any:

        """ """

        widsamps = int(round(width / self.tsamp))
        runmedian = fastrmed(
            self.data,
            widsamps,
            minpts,
        )

        if inplace:
            self.data = self.data - runmedian
            return None
        else:
            return TimeSeries(
                self.data - runmedian,
                tsamp=self.tsamp,
                meta=self.meta,
            )

    def downsample(
        self: T,
        factor: float,
        inplace: bool = False,
    ) -> Any:

        """ """

        if inplace:
            self.data = dsamp(self.data, factor)
            self.tsamp = self.tsamp * factor
            return None
        else:
            data = dsamp(self.data, factor)
            tsamp = self.tsamp * factor
            return TimeSeries(
                data,
                tsamp,
                meta=self.meta,
            )

    @meta.requires(["nsamp", "tsamp"])
    def fold(
        self,
        period: float,
        bins: int,
        subints: Optional[int] = None,
    ) -> np.ndarray:

        """ """

        nsamp = self.meta["nsamp"]
        tsamp = self.meta["tsamp"]

        return fold(
            self,
            period,
            nsamp,
            tsamp,
            bins,
            subints=subints,
        )

    @classmethod
    def generate(
        cls: Type[T],
        length: float,
        tsamp: float,
        period: float,
        phi0: float = 0.5,
        ducy: float = 0.02,
        amp: float = 10.0,
        stdnoise: float = 1.0,
    ) -> T:

        """ """

        nsamp = int(round(length / tsamp))
        period_samples = period / tsamp
        data = generate(
            nsamp,
            period_samples,
            phi0=phi0,
            ducy=ducy,
            amp=amp,
            stdnoise=stdnoise,
        )

        meta = Metadata(
            {
                "source_name": "fake",
                "signal_shape": "Von Mises",
                "signal_period": period,
                "signal_initial_phase": phi0,
                "signal_duty_cycle": ducy,
            }
        )
        return cls(
            data,
            tsamp,
            meta=meta,
            copy=False,
        )

    @classmethod
    def fromnpy(
        cls: Type[T],
        array: np.ndarray,
        tsamp: float,
        copy: bool = False,
    ) -> T:

        """"""

        return cls(
            array,
            tsamp,
            copy=copy,
        )

    @classmethod
    def frombin(
        cls: Type[T],
        fname: str,
        dtype: np.dtype,
        tsamp: float,
    ) -> T:

        """"""

        data = np.fromfile(fname, dtype=dtype)
        return cls.fromnpy(
            data,
            tsamp,
            copy=False,
        )

    @classmethod
    def fromnpyfile(
        cls: Type[T],
        fname: str,
        tsamp: float,
    ) -> T:

        """"""

        data = np.load(fname)
        return cls(
            data,
            tsamp,
            copy=False,
        )

    @classmethod
    def fromdat(
        cls: Type[T],
        f: str,
    ) -> T:

        """"""

        meta, data = datread(f)
        tsamp = meta["tsamp"]
        return cls(
            data,
            tsamp=tsamp,
            meta=meta,
        )

    @classmethod
    def fromtim(
        cls: Type[T],
        f: str,
    ) -> T:

        """"""

        meta, data = timread(f)
        tsamp = meta["tsamp"]
        return cls(
            data,
            tsamp=tsamp,
            meta=meta,
        )

    def tonpy(self) -> np.ndarray:

        """"""

        return self.data

    def todat(
        self,
        f: str,
    ) -> None:

        """"""

        if self.meta:
            datwrite(
                self.data,
                self.meta,
                f,
            )

    def totim(
        self,
        f: str,
    ) -> None:

        """"""

        if self.meta:
            timwrite(
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
