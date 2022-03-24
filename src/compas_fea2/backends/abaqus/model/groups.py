from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import NodesGroup
from compas_fea2.model import ElementsGroup
from compas_fea2.model.groups import FacesGroup


def _generate_jobdata(self, instance):
    """Generates the string information for the input file.

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

    if self.generate:
        data_section.append(', '.join([line, 'generate']))
        data_section.append(f'{self.keys[0]}, {self.keys[-1]}, 1')
    else:
        data_section.append(line)
        data = [str(s+1) for s in self.keys]
        chunks = [data[x:x+15] for x in range(0, len(data), 15)]  # split data for readibility
        for chunk in chunks:
            data_section.append(', '.join(chunk))
    return '\n'.join(data_section) + '\n'


class AbaqusNodesGroup(NodesGroup):
    """Initialises the Set object.

    Parameters
    ----------
    generate : bool
        Automatically generates a set of elements/nodes between the two keys specified.

    Notes
    -----
    This is equivalent to a node set in Abaqus

    """

    def __init__(self, name, nodes_keys, generate=False):
        super(AbaqusNodesGroup, self).__init__(name, nodes_keys)
        self._generate = generate
        self._set_type = 'nset'

    @property
    def generate(self):
        """The generate property."""
        return self._generate

    def _generate_jobdata(self, instance=None):
        return _generate_jobdata(self, instance)


class AbaqusElementsGroup(ElementsGroup):
    """Initialises the Set object.

    Parameters
    ----------
    generate : bool
        Automatically generates a set of elements/nodes between the two keys specified.

    Notes
    -----
    This is equivalent to a node set in Abaqus

    """

    def __init__(self, name, elements_keys, generate=False):
        super(AbaqusElementsGroup, self).__init__(name, elements_keys)
        self._generate = generate
        self._set_type = 'elset'

    @property
    def generate(self):
        """bool : if ``True``, automatically generates a set of elements/nodes between the two keys specified."""
        return self._generate

    def _generate_jobdata(self, instance=None):
        return _generate_jobdata(self, instance)


class AbaqusFacesGroup(FacesGroup):
    """Abaqus implementation of the :class:`compas_fea2.model.FacesGroup`.\n
    """
    __doc__ += FacesGroup.__doc__

    def __init__(self, name, part, element_face):
        super(FacesGroup, self).__init__(name, part, element_face)

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
