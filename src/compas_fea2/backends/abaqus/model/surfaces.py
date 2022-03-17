from compas_fea2.model.surfaces import SurfaceBase


class Surface(SurfaceBase):
    """Abaqus implementation of the :class:`SurfaceBase`.\n
    """
    __doc__ += SurfaceBase.__doc__

    def __init__(self, name, part, element_face):
        super(Surface, self).__init__(name, part, element_face)

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        str
            input file data line.
        """
        lines = [f'*Surface, type=ELEMENT, name={self._name}']
        for key, face in self._element_face.items():
            lines.append(f'{self._part}-1.{key+1}, {face}')
        lines.append('**\n')
        return '\n'.join(lines)
