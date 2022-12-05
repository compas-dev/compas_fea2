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
    name = self.name if not instance else '{}_i'.format(self.name)
    line = '*{0}, {0}={1}'.format(self._set_type, name)
    if instance:
        line = ', instance='.join([line, self.part.name+'-1'])

    data_section.append(line)
    data = [str(member.key+1) for member in self._members]
    chunks = [data[x:x+15] for x in range(0, len(data), 15)]  # split data for readibility
    for chunk in chunks:
        data_section.append(', '.join(chunk))
    return '\n'.join(data_section)


class AbaqusNodesGroup(NodesGroup):
    """Abaqus implementation of :class:`NodesGroup`

    Notes
    -----
    This is equivalent to a node set in Abaqus

    """
    __doc__ += NodesGroup.__doc__

    def __init__(self, *, nodes, name=None, **kwargs):
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

    def __init__(self,  *, elements, name=None, **kwargs):
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

    def __init__(self, *, faces, name=None, **kwargs):
        super(AbaqusFacesGroup, self).__init__(faces=faces, name=name, **kwargs)

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
        lines = ['*Surface, type=ELEMENT, name={}_i'.format(self._name)]
        for face in self.faces:
            lines.append('{}-1.{}, {}'.format(self.part.name, face.element.key+1, face.tag))
        lines.append('**')
        return '\n'.join(lines)


class AbaqusPartsGroup(PartsGroup):
    """Abaqus implementation of the :class:`PartsGroup`.\n"""
    __doc__ += PartsGroup.__doc__

    def __init__(self, *, parts, model=None, name=None, **kwargs):
        super(AbaqusPartsGroup, self).__init__(parts=parts, model=model, name=name, **kwargs)
        raise NotImplementedError
