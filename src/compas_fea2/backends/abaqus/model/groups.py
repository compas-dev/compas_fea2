from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import NodesGroup
from compas_fea2.model import ElementsGroup
from compas_fea2.model.groups import FacesGroup, PartsGroup


def _generate_jobdata(self, instance):
    """Generates the common string information for the input file for all the
    groups.

    Parameters
    ----------
    instance: bool
        if ``True`` the set is generated at the instance level, otherwise only
        at the part level

    Returns
    -------
    input file data line (str).
    """
    data_section = []
    name = self.name if not instance else f'{self.name}_{instance}'
    line = f'*{self._set_type}, {self._set_type}={name}'
    if instance:
        # BUG instance is a bool, but it should be a str with the name of the instance
        line = ', instance='.join([line, instance])

    data_section.append(line)
    data = [str(el.key+1) for el in self.elements]
    chunks = [data[x:x+15] for x in range(0, len(data), 15)]  # split data for readibility
    for chunk in chunks:
        data_section.append(', '.join(chunk))
    return '\n'.join(data_section) + '\n'


class AbaqusNodesGroup(NodesGroup):
    """Abaqus implementation of :class:`NodesGroup`

    Notes
    -----
    This is equivalent to a node set in Abaqus

    """
    __doc__ += NodesGroup.__doc__

    def __init__(self, nodes, name=None, **kwargs):
        super(AbaqusNodesGroup, self).__init__(nodes=nodes, name=name, **kwargs)
        self._set_type = 'nset'

    def _generate_jobdata(self, instance=None):
        return _generate_jobdata(self, instance)


class AbaqusElementsGroup(ElementsGroup):
    """Abaqus implementation of :class:`ElementsGroup`

    Notes
    -----
    This is equivalent to a element set in Abaqus

    """
    __doc__ += ElementsGroup.__doc__

    def __init__(self, *, elements, name=None, **kwargs):
        super(AbaqusElementsGroup, self).__init__(elements=elements, name=name, **kwargs)
        self._set_type = 'elset'

    def _generate_jobdata(self, instance=None):
        return _generate_jobdata(self, instance)


class AbaqusFacesGroup(FacesGroup):
    """Abaqus implementation of :class:`NodesGroup`

    Notes
    -----
    This is equivalent to a `Surface` in Abaqus

    """
    __doc__ += NodesGroup.__doc__

    def __init__(self, *, part, element_face, name=None, **kwargs):
        super(FacesGroup, self).__init__(part=part, element_face=element_face, name=name, **kwargs)

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


class AbaqusPartsGroup(PartsGroup):
    """Abaqus implementation of the :class:`PartsGroup`.\n"""
    __doc__ += PartsGroup.__doc__

    def __init__(self, *, parts, name=None, **kwargs):
        super(AbaqusPartsGroup, self).__init__(parts=parts, name=name, **kwargs)
        raise NotImplementedError
