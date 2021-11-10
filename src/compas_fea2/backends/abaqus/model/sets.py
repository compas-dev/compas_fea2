
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.model import SetBase
from compas_fea2.backends._base.model import SurfaceBase

# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'Set',
    'Surface',
]


class Set(SetBase):

    """Initialises the Set object.

    Parameters
    ----------
    name : str
        Name of the set.
    selection : list
        A list with either the Node or Element objects belonging to the set.
    stype : str
        Node or Element set identifier. It can be either 'nset' or 'elset'
    generate : bool
        Automatically generates a set of elements/nodes between the two keys specified.
    """

    # TODO generate option might not be a good idea!
    def __init__(self, name, selection, stype, generate=False):
        super(Set, self).__init__(name, selection, stype, generate)

    def _generate_data(self):
        data_section = []
        line = '*{}, {}={}'.format(self.stype, self.stype, self.name)
        if self.instance:
            line = ', instance='.join([line, self.instance])
        if self.generate:
            line = ', '.join([line, 'generate'])
            data_section.append(line)
            data_section.append('{0}, {1}, 1'.format(self.selection[0].key, self.selection[-1].key))
        else:
            data_section.append(line)
            data = []
            for s in self.selection:
                data.append(str(s+1))
            chunks = [data[x:x+15] for x in range(0, len(data), 15)]
            for chunk in chunks:
                data_section.append(', '.join(chunk))
        return '\n'.join(data_section) + '\n'


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

        self._jobdata = self._generate_data()

    @property
    def jobdata(self):
        """This property is the representation of the object in a software-specific inout file.

        Returns
        -------
        str

        Examples
        --------
        >>>
        """
        return self._jobdata

    # TODO: old ---> change
    def _generate_data(self):
        line = '*Surface, type={}, NAME={0}'.format(self.stype, self.name)
        self.write_line('** ELEMENT, SIDE')

        for element, sides in element_set.selection.items():
            for side in sides:
                self.write_line('{0}, {1}'.format(element + 1, side))
                self.blank_line()
