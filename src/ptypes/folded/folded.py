import attr
import typing
import numpy as np  # type: ignore

from ptypes.metadata import NoMeta, Metadata

from .formats import (
    arread,
    arwrite,
    pfdread,
    pfdwrite,
    bprofread,
    bprofwrite,
)


P = typing.TypeVar("P", bound="Profile")
S = typing.TypeVar("S", bound="Slice")
F = typing.TypeVar("F", bound="Folded")


@attr.s(auto_attribs=True)
class Profile(object):

    """"""

    data: np.ndarray

    wid: int
    pos: int
    nbin: int

    bsline: np.ndarray

    meta: typing.Optional[Metadata] = None

    @classmethod
    def _wid(
        cls: typing.Type[P],
        data: np.ndarray,
    ) -> int:

        """"""

        median = np.median(data)
        data = data - median
        trywids = np.arange(
            1,
            data.size,
        )

        convmaxs = np.array(
            [
                np.convolve(
                    np.ones(trywid),
                    data,
                    mode="same",
                ).max()
                / np.sqrt(trywid)
                for trywid in trywids
            ]
        )

        wid = trywids[convmaxs.argmax()]

        return wid

    @classmethod
    def _pos(
        cls: typing.Type[P],
        wid: int,
        data: np.ndarray,
    ) -> int:

        """"""

        pos = np.convolve(
            np.ones(wid),
            data,
            mode="same",
        ).argmax()

        return pos

    @classmethod
    def _bsline(
        cls: typing.Type[P],
        wid: int,
        pos: int,
        data: np.ndarray,
    ) -> np.ndarray:

        """"""

        wing = int(np.ceil(wid / 2.0))

        bsline = np.hstack(
            (
                data[: pos - wing],
                data[pos + wing + 1 :],
            )
        )

        return bsline

    def dirtysnr(self) -> float:

        """"""

        copy = self.data.copy()
        copy = copy - self.bsline.mean()
        copy = copy / self.bsline.std()
        return float(copy.sum() / np.sqrt(self.wid))

    def cleansnr(self) -> None:

        """"""

        # TODO: Write this function using Morello's spyden module.

        pass

    @classmethod
    def fromnp(
        cls: typing.Type[P],
        data: np.ndarray,
        meta: typing.Optional[Metadata] = None,
    ) -> P:

        """"""

        wid = cls._wid(data)
        pos = cls._pos(wid, data)
        bsline = cls._bsline(wid, pos, data)

        nbin = data.size

        return cls(
            data,
            wid=wid,
            pos=pos,
            bsline=bsline,
            nbin=nbin,
            meta=meta,
        )

    @classmethod
    def frombprof(
        cls: typing.Type[P],
        f: str,
    ) -> P:

        """"""

        m, d = bprofread(f)
        meta = Metadata.fromdict(m)
        return cls.fromnp(d, meta=meta)


@attr.s(auto_attribs=True)
class Slice(object):

    """"""

    data: np.ndarray

    nint: int
    nsub: int

    @classmethod
    def fromnp(
        cls: typing.Type[S],
        data: np.ndarray,
    ) -> S:

        """"""

        (nint, nsub) = data.shape
        return cls(
            data,
            nint,
            nsub,
        )

    def profile(self) -> Profile:

        """"""

        profile = self.data.sum(axis=0)
        return Profile.fromnp(profile)

    def normalise(self) -> np.ndarray:

        """"""

        mean = self.data.mean(axis=1)
        mean = mean.reshape(self.nint, 1)
        norm = self.data / mean
        return norm


@attr.s(auto_attribs=True)
class Folded(object):

    """"""

    data: np.ndarray

    nint: int
    nsub: int
    nbin: int

    meta: typing.Optional[Metadata] = None

    def subint(self, nint: int) -> Slice:

        """"""

        return Slice.fromnp(self.data[nint])

    def subband(self, nsub: int) -> Slice:

        """"""

        return Slice.fromnp(self.data[:, nsub])

    def timphase(self) -> Slice:

        """"""

        return Slice.fromnp(self.data.sum(axis=0))

    def freqphase(self) -> Slice:

        """"""

        return Slice.fromnp(self.data.sum(axis=1))

    def profile(self) -> Profile:

        """"""

        return Profile.fromnp(self.data.sum(axis=0).sum(axis=1))

    @classmethod
    def fromnp(
        cls: typing.Type[F],
        data: np.ndarray,
        meta: typing.Optional[Metadata] = None,
    ) -> F:

        """"""

        (
            nint,
            nsub,
            nbin,
        ) = data.shape
        return cls(
            data,
            nint=nint,
            nsub=nsub,
            nbin=nbin,
            meta=meta,
        )

    @classmethod
    def fromar(
        cls: typing.Type[F],
        f: str,
    ) -> F:

        """"""

        pass

    @classmethod
    def frompfd(
        cls: typing.Type[F],
        f: str,
    ) -> F:

        """"""

        d = pfdread(f)
        cube = d.get("profs", None)
        d.pop("profs")
        meta = Metadata.fromdict(d)
        return cls.fromnp(data=cube, meta=meta)

    def toar(self) -> None:
        pass

    def topfd(self, f: str) -> None:

        """"""

        if self.meta:
            d: typing.Dict[
                str,
                typing.Any,
            ] = {}
            d.update(self.meta.todict())
            d["profs"] = self.data

            return pfdwrite(d, f)
        else:
            raise NoMeta(
                """
                Metadata absent.
                Cannot write to a *.pfd file.
                Exiting...
                """
            )
