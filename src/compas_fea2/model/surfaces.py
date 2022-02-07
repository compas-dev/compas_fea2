from compas_fea2.base import FEABase


class SurfaceBase(FEABase):
    def __init__(self, name, part, element, face):
        self._name = name
        self._part = part
        self._element = element
        self._face = face
