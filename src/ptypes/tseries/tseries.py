import attr
import copy
import typing
import numpy as np  # type: ignore

from pathlib import Path
from ptypes.metadata import (
    NoMeta,
    Metadata,
)

from .formats import (
    datread,
    datwrite,
    timread,
    timwrite,
)


T = typing.TypeVar("T", bound="TimeSeries")


def downsamp(
    data: np.ndarray,
    factor: typing.Union[int, float],
) -> np.ndarray:

    """"""

    pass


def tscrunch(
    data: np.ndarray,
    factor: typing.Union[int, float],
) -> np.ndarray:

    """"""

    factor = int(factor)
    if factor <= 1:
        return data
    N = (data.size // factor) * factor
    return data[:N].reshape(-1, factor).mean(axis=1)


def fastrmed(
    data: np.ndarray,
    widsamps: int,
    minpts: int,
) -> np.ndarray:

    """"""

    pass


def generate(
    nsamp: int,
    period: float,
    phi0: float = 0.5,
    ducy: float = 0.02,
    amp: float = 10.0,
    stdnoise: float = 1.0,
) -> np.ndarray:

    """"""

    kappa = np.log(2.0) / (2.0 * np.sin(np.pi * ducy / 2.0) ** 2)

    phrads = (
        np.arange(
            nsamp,
        )
        / period
        - phi0
    ) * (2 * np.pi)
    signal = np.exp(kappa * (np.cos(phrads) - 1.0))
    scaler = amp * (signal ** 2).sum() ** -0.5
    signal = scaler * signal

    if stdnoise > 0.0:
        noise = np.random.normal(
            size=nsamp,
            loc=0.0,
            scale=stdnoise,
        )
    else:
        noise = 0.0

    tseries = signal + noise
    return tseries


def fold(
    ts: T,
    period: float,
    bins: int,
    subints: typing.Optional[int] = None,
) -> np.ndarray:

    """"""

    pass


@attr.s(auto_attribs=True)
class TimeSeries(object):

    """"""

    data: np.ndarray

    tsamp: float

    meta: typing.Optional[Metadata] = None

    _copy: bool = False

    def copy(self: T) -> T:

        """"""

        return copy.deepcopy(self)

    def normalise(
        self: T,
        inplace: bool = False,
    ) -> typing.Any:

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
    ) -> typing.Any:

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
    ) -> typing.Any:

        """ """

        if inplace:
            self.data = downsamp(self.data, factor)
            self.tsamp = self.tsamp * factor
            return None
        else:
            data = downsamp(self.data, factor)
            tsamp = self.tsamp * factor
            return TimeSeries(
                data,
                tsamp,
                meta=self.meta,
            )

    def fold(
        self,
        period: float,
        bins: int,
        subints: typing.Optional[int] = None,
    ) -> np.ndarray:

        """ """

        return fold(
            self,
            period,
            bins,
            subints=subints,
        )

    @classmethod
    def generate(
        cls: typing.Type[T],
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
        cls: typing.Type[T],
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
        cls: typing.Type[T],
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
        cls: typing.Type[T],
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
        cls: typing.Type[T],
        f: str,
    ) -> T:

        """"""

        meta, data = datread(f)
        return cls(
            data,
            tsamp=meta["tsamp"],
            meta=meta,
        )

    @classmethod
    def fromtim(
        cls: typing.Type[T],
        f: str,
    ) -> T:

        """"""

        meta, data = timread(f)
        return cls(
            data,
            tsamp=meta["tsamp"],
            meta=meta,
        )

    def todat(
        self,
        f: typing.Optional[str] = None,
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
            raise NoMeta("Metadata absent. Cannot write to a *.tim file. Exiting...")

    def tonpy(self) -> None:
        pass
