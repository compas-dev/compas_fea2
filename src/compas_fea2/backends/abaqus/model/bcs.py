from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.model import GeneralBCBase
from compas_fea2.backends._base.model import FixedBCBase
from compas_fea2.backends._base.model import PinnedBCBase
from compas_fea2.backends._base.model import FixedBCXXBase
from compas_fea2.backends._base.model import FixedBCYYBase
from compas_fea2.backends._base.model import FixedBCZZBase
from compas_fea2.backends._base.model import RollerBCXBase
from compas_fea2.backends._base.model import RollerBCYBase
from compas_fea2.backends._base.model import RollerBCZBase
from compas_fea2.backends._base.model import RollerBCXYBase
from compas_fea2.backends._base.model import RollerBCYZBase
from compas_fea2.backends._base.model import RollerBCXZBase

# Author(s): Francesco Ranaudo (github.com/franaudo)

# TODO: add the possibility to add bcs to nodes/elements and not only to sets


dofs = ['x',  'y',  'z',  'xx', 'yy', 'zz']


def _generate_jobdata(obj):
    """Generates the string information for the input file.

    Parameters
    ----------
    None

    Returns
    -------
    input file data line (str).
    """
    data_section = []
    line = ("** Name: {} Type: BC/Rotation\n"
            "*Boundary, op=NEW").format(obj.name)
    data_section.append(line)
    c = 1
    for dof in dofs:
        if dof in obj._components.keys() and obj._components[dof] != None:
            if not obj.components[dof]:
                line = """{}, {}, {}""".format(obj.bset, c, c)
            else:
                line = """{}, {}, {}, {}""".format(obj.bset, c, c, obj._components[dof])
            data_section.append(line)
        c += 1
    return '\n'.join(data_section) + '\n'


class GeneralBC(GeneralBCBase):

    def __init__(self, name, bset, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global'):
        super(GeneralBC, self).__init__(name, None, x, y, z, xx, yy, zz, axes)
        self.bset = bset
        self._modify = True

    def _generate_jobdata(self):
        return _generate_jobdata(self)


class FixedBC(FixedBCBase):

    def __init__(self, name, bset, axes='global'):
        super(FixedBC, self).__init__(name, None, axes)
        self.bset = bset

    def _generate_jobdata(self):
        return _generate_jobdata(self)


class PinnedBC(PinnedBCBase):

    def __init__(self, name, bset=None, nodes=None, axes='global'):
        super(PinnedBC, self).__init__(name, None, axes)
        if not bset and nodes:
            raise ValueError('You must specify either a node or a set')
        if bset and nodes:
            raise ValueError('You cannot specify both a node and a set')
        if bset:
            self.bset = bset.name  # TODO change
            self.nodes = bset.selection

    def _generate_jobdata(self):
        return _generate_jobdata(self)


class FixedBCXX(FixedBCXXBase):

    def __init__(self, name, bset, axes='global'):
        super(FixedBCXX, self).__init__(name, None, axes)
        self.bset = bset

    def _generate_jobdata(self):
        return _generate_jobdata(self)


class FixedBCYY(FixedBCYYBase):

    def __init__(self, name, bset, axes='global'):
        super(FixedBCYY, self).__init__(name, None, axes)
        self.bset = bset

    def _generate_jobdata(self):
        return _generate_jobdata(self)


class FixedBCZZ(FixedBCZZBase):

    def __init__(self, name, bset, axes='global'):
        super(FixedBCZZ, self).__init__(name, None, axes)
        self.bset = bset

    def _generate_jobdata(self):
        return _generate_jobdata(self)


class RollerBCX(RollerBCXBase):

    def __init__(self, name, bset, axes='global'):
        super(RollerBCX, self).__init__(name, None, axes)
        self.bset = bset

    def _generate_jobdata(self):
        return _generate_jobdata(self)


class RollerBCY(RollerBCYBase):

    def __init__(self, name, bset, axes='global'):
        super(RollerBCY, self).__init__(name, None, axes)
        self.bset = bset

    def _generate_jobdata(self):
        return _generate_jobdata(self)


class RollerBCZ(RollerBCZBase):

    def __init__(self, name, bset, axes='global'):
        super(RollerBCZ, self).__init__(name, None, axes)
        self.bset = bset

    def _generate_jobdata(self):
        return _generate_jobdata(self)


class RollerBCXY(RollerBCXYBase):

    def __init__(self, name, bset, axes='global'):
        super(RollerBCXY, self).__init__(name, None, axes)
        self.bset = bset

    def _generate_jobdata(self):
        return _generate_jobdata(self)


class RollerBCYZ(RollerBCYZBase):

    def __init__(self, name, bset, axes='global'):
        super(RollerBCYZ, self).__init__(name, None, axes)
        self.bset = bset

    def _generate_jobdata(self):
        return _generate_jobdata(self)


class RollerBCXZ(RollerBCXZBase):

    def __init__(self, name, bset, axes='global'):
        super(RollerBCXZ, self).__init__(name, None, axes)
        self.bset = bset

    def _generate_jobdata(self):
        return _generate_jobdata(self)


if __name__ == "__main__":
    d = RollerBCXZ(name='bc_roller', bset='roller')
    print(d._generate_jobdata())
