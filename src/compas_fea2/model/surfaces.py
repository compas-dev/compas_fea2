from compas_fea2.base import FEAData


class Surface(FEAData):
    def __init__(self, name, part, element, face):
        super(Surface, self).__init__(name=name)
        self._name = name
        self._part = part
        self._element = element
        self._face = face
