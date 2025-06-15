from typing import TYPE_CHECKING
from typing import Union

from compas_fea2.base import FEAData

if TYPE_CHECKING:
    from .elements import BeamElement


class _BeamEndRelease(FEAData):
    """Assign a general end release to a `compas_fea2.model.BeamElement`.

    Parameters
    ----------
    n : bool, optional
        Release displacements along the local axial direction, by default False
    v1 : bool, optional
        Release displacements along local 1 direction, by default False
    v2 : bool, optional
        Release displacements along local 2 direction, by default False
    m1 : bool, optional
        Release rotations about local 1 direction, by default False
    m2 : bool, optional
        Release rotations about local 2 direction, by default False
    t : bool, optional
        Release rotations about local axial direction (torsion), by default False

    Attributes
    ----------
    location : str
        'start' or 'end'
    element : :class:`compas_fea2.model.BeamElement`
        The element to release.
    n : bool
        Release displacements along the local axial direction, by default False
    v1 : bool
        Release displacements along local 1 direction, by default False
    v2 : bool
        Release displacements along local 2 direction, by default False
    m1 : bool
        Release rotations about local 1 direction, by default False
    m2 : bool
        Release rotations about local 2 direction, by default False
    t : bool
        Release rotations about local axial direction (torsion), by default False

    """

    def __init__(
        self,
        n: bool = False,
        v1: bool = False,
        v2: bool = False,
        m1: bool = False,
        m2: bool = False,
        t: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._element: Union["BeamElement", None] = None
        self._location: Union[str, None] = None
        self.n: bool = n
        self.v1: bool = v1
        self.v2: bool = v2
        self.m1: bool = m1
        self.m2: bool = m2
        self.t: bool = t

    @property
    def element(self) -> Union["BeamElement", None]:
        return self._element

    @element.setter
    def element(self, value: "BeamElement"):
        if not isinstance(value, "BeamElement"):
            raise TypeError(f"{value!r} is not a beam element.")
        self._element = value

    @property
    def location(self) -> Union[str, None]:
        return self._location

    @location.setter
    def location(self, value: str):
        if value not in ("start", "end"):
            raise TypeError("the location can be either `start` or `end`")
        self._location = value

    @property
    def __data__(self):
        return {
            "class": self.__class__.__base__.__name__,
            "element": self._element,
            "location": self._location,
            "n": self.n,
            "v1": self.v1,
            "v2": self.v2,
            "m1": self.m1,
            "m2": self.m2,
            "t": self.t,
        }

    @classmethod
    def __from_data__(cls, data):
        obj = cls(
            n=data["n"],
            v1=data["v1"],
            v2=data["v2"],
            m1=data["m1"],
            m2=data["m2"],
            t=data["t"],
        )
        obj._element = data["element"]
        obj._location = data["location"]
        return obj


class BeamEndPinRelease(_BeamEndRelease):
    """Assign a pin end release to a `compas_fea2.model.BeamElement`.

    Parameters
    ----------
    m1 : bool, optional
        Release rotations about local 1 direction, by default False
    m2 : bool, optional
        Release rotations about local 2 direction, by default False
    t : bool, optional
        Release rotations about local axial direction (torsion), by default False

    """

    def __init__(self, m1: bool = False, m2: bool = False, t: bool = False, **kwargs):
        super().__init__(n=False, v1=False, v2=False, m1=m1, m2=m2, t=t, **kwargs)


class BeamEndSliderRelease(_BeamEndRelease):
    """Assign a slider end release to a `compas_fea2.model.BeamElement`.

    Parameters
    ----------
    v1 : bool, optional
        Release displacements along local 1 direction, by default False
    v2 : bool, optional
        Release displacements along local 2 direction, by default False

    """

    def __init__(self, v1: bool = False, v2: bool = False, **kwargs):
        super().__init__(v1=v1, v2=v2, n=False, m1=False, m2=False, t=False, **kwargs)
