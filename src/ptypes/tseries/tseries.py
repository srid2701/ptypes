import attr
import copy
import typing
import numpy as np  # type: ignore

from pathlib import Path

from ptypes.metadata import Metadata


T = typing.TypeVar("T", bound="TimeSeries")


@attr.s(auto_attribs=True)
class TimeSeries(object):

    """"""

    data: np.ndarray

    tsamp: float

    meta: typing.Optional[
        typing.Union[
            dict,
            Metadata,
        ]
    ] = None

    copy: bool = False

    def copy(self) -> TimeSeries:

        """"""

        return copy.deepcopy(self)

    def normalise(
        self,
        inplace: bool = False,
    ) -> typing.Union[None, TimeSeries]:

        """"""

        v = self.data.var(dtype=np.float64)
        m = self.data.mean(dtype=np.float64)

        norm = v ** 0.5

        if inplace:
            self.data = (self.data - m) / norm
        else:
            return TimeSeries(
                (self.data - m) / norm,
                tsamp=self.tsamp,
                meta=self.meta,
            )

    def deredden(
        self,
        width: float,
        minpts: int = 10,
        inplace: bool = False,
    ) -> typing.Union[None, TimeSeries]:

        """"""

        widsamps = int(round(width / self.tsamp))
        runmedian = fastrmed(
            self.data,
            widsamps,
            minpts,
        )

        if inplace:
            self.data = self.data - runmedian
        else:
            return TimeSeries(
                self.data - runmedian,
                tsamp=self.tsamp,
                meta=self.meta,
            )

    def downsample(
        self,
        factor: float,
        inplace: bool = False,
    ) -> typing.Union[None, TimeSeries]:

        """"""

        if inplace:
            self.data = downsample(self.data, factor)
            self.tsamp = self.tsamp * factor
        else:
            data = downsample(self.data, factor)
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

        """"""

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
        amplitude: float = 10.0,
        stdnoise: float = 1.0,
    ) -> T:

        """"""

        nsamp = int(round(length / tsamp))
        period_samples = period / tsamp
        data = generate(
            nsamp,
            period_samples,
            phi0=phi0,
            ducy=ducy,
            amplitude=amplitude,
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
        fname: str,
    ) -> T:

        """"""

        pass

    @classmethod
    def fromtim(
        cls: typing.Type[T],
        fname: str,
    ) -> T:

        """"""

        pass

    def todat():
        pass

    def totim():
        pass

    def tonpy():
        pass
