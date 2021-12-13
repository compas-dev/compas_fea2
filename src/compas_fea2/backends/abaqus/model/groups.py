
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.model.groups import NodesGroupBase
from compas_fea2.backends._base.model.groups import ElementsGroupBase
from compas_fea2.backends._base.model.groups import SurfaceBase

# Author(s): Francesco Ranaudo (github.com/franaudo)


def _generate_jobdata(self):
    """Generates the string information for the input file.

    Parameters
    ----------
    None

    Returns
    -------
    input file data line (str).
    """
    data_section = []
    line = f'*{self._set_type}, {self._set_type}={self.name}'
    if self.instance:
        line = ', instance='.join([line, self.instance])
    if self.generate:
        data_section.append(', '.join([line, 'generate']))
        data_section.append(f'{self.selection[0].key}, {self.selection[-1].key}, 1')
    else:
        data_section.append(line)
        data = [str(s+1) for s in self.selection]
        chunks = [data[x:x+15] for x in range(0, len(data), 15)]  # split data for readibility
        for chunk in chunks:
            data_section.append(', '.join(chunk))
    return '\n'.join(data_section) + '\n'


class NodesGroup(NodesGroupBase):

    """Initialises the Set object.

    Notes
    -----
    This is equivalent to a node set in Abaqus

    Parameters
    ----------
    generate : bool
        Automatically generates a set of elements/nodes between the two keys specified.
    """

    def __init__(self, name, selection, generate=False):
        super(NodesGroup, self).__init__(name, selection)
        self._generate = generate
        self._set_type = 'nset'

    @property
    def generate(self):
        """The generate property."""
        return self._generate

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return _generate_jobdata(self)


class ElementsGroup(ElementsGroupBase):

    """Initialises the Set object.

    Notes
    -----
    This is equivalent to a node set in Abaqus

    Parameters
    ----------
    generate : bool
        Automatically generates a set of elements/nodes between the two keys specified.
    """

    def __init__(self, name, selection, generate=False):
        super(ElementsGroup, self).__init__(name, selection)
        self._generate = generate
        self._set_type = 'elset'

    @property
    def generate(self):
        """The generate property."""
        return self._generate

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return _generate_jobdata(self)


class Surface(SurfaceBase):
    """Initialises the Surfaces object.

    Parameters
    ----------
    name : str
        Name of the set.
    selection : list
        A list with either the Node or Element objects belonging to the set.
    generate : bool
        Automatically generates a set of elements/nodes between the two keys specified.
    """

    # TODO check http://130.149.89.49:2080/v6.14/books/usb/default.htm?startat=pt01ch02s03aus17.html#usb-int-adeformablesurf
    def __init__(self, name, set, generate=False):
        super(Surface, self).__init__(name, set, generate)

    # TODO: old ---> change
    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        line = '*Surface, type={}, NAME={0}'.format(self.stype, self.name)
        self.write_line('** ELEMENT, SIDE')

        for element, sides in element_set.selection.items():
            for side in sides:
                self.write_line('{0}, {1}'.format(element + 1, side))
                self.blank_line()