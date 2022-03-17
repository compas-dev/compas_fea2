from compas_fea2.base import FEAData


<<<<<<< HEAD:src/compas_fea2/model/surfaces.py
class Surface(FEAData):
    def __init__(self, name, part, element, face):
        super(Surface, self).__init__(name=name)
=======
class SurfaceBase(FEABase):
    """Surface class. It cgroups together elements faces.

    Parameters
    ----------
    name : str
        name of the Surface
    part : obj
        :class:`PartBase` subclass object where the surface is located
    element_face : dict
        element_key, face pairs of the elements faces creating the surface
    """

    def __init__(self, name, part, element_face):
>>>>>>> 0fcf42ed8e1eb38788d736a3e47f207522be8a7c:src/compas_fea2/_base/model/surfaces.py
        self._name = name
        self._part = part
        self._element_face = element_face

    @property
    def name(self):
        """str : name of the Surface"""
        return self._name

    @property
    def part(self):
        """obj : :class:`PartBase` subclass object where the surface is located"""
        return self._part

    @property
    def element_face(self):
        """dict : element_key, face pairs of the elements faces creating the surface"""
        return self._element_face

    def __repr__(self):
        return '{0}({1})'.format(self.__name__, self.name)
