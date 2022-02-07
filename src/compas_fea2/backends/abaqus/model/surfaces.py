from compas_fea2.model.surfaces import SurfaceBase


class Surface(SurfaceBase):
    def __init__(self, name, part, element, face):
        super(Surface, self).__init__(name, part, element, face)

    def _generate_jobdata(self):
        return f"""*Surface, type=ELEMENT, name={self._name}
{self._part}-1.{self._element}, {self._face}\n"""
