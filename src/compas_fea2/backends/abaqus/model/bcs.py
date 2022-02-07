from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# from compas_fea2.model import GeneralBCBase
from compas_fea2.model import FixedBCBase
from compas_fea2.model import PinnedBCBase
from compas_fea2.model import FixedBCXXBase
from compas_fea2.model import FixedBCYYBase
from compas_fea2.model import FixedBCZZBase
from compas_fea2.model import RollerBCXBase
from compas_fea2.model import RollerBCYBase
from compas_fea2.model import RollerBCZBase
from compas_fea2.model import RollerBCXYBase
from compas_fea2.model import RollerBCYZBase
from compas_fea2.model import RollerBCXZBase

# Author(s): Francesco Ranaudo (github.com/franaudo)

# TODO: add the possibility to add bcs to nodes/elements and not only to sets


dofs = ['x',  'y',  'z',  'xx', 'yy', 'zz']


def _generate_jobdata(obj, instance, nodes):
    """Generates the string information for the input file.

    Parameters
    ----------
    None

    Returns
    -------
    input file data line (str).
    """
    data_section = [f'** Name: {obj.name} Type: BC/Rotation\n',
                    '*Boundary, op=NEW']
    for node in nodes:
        for comp, dof in enumerate(dofs, 1):
            if dof in obj.components:
                data_section += [f'{instance}.{node+1}, {comp}, {obj.components[dof]}']
    return '\n'.join(data_section)


# class GeneralBC(GeneralBCBase):

#     def __init__(self, name, axes='global'):
#         super(GeneralBC, self).__init__(name, x, y, z, xx, yy, zz, axes)
#         self._modify = True

#     def _generate_jobdata(self):
#         return _generate_jobdata(self)


class FixedBC(FixedBCBase):

    def __init__(self, name, axes='global'):
        super(FixedBC, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class PinnedBC(PinnedBCBase):

    def __init__(self, name, axes='global'):
        super(PinnedBC, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class FixedBCXX(FixedBCXXBase):

    def __init__(sself, name, axes='global'):
        super(FixedBCXX, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class FixedBCYY(FixedBCYYBase):

    def __init__(self, name, axes='global'):
        super(FixedBCYY, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class FixedBCZZ(FixedBCZZBase):

    def __init__(self, name, axes='global'):
        super(FixedBCZZ, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class RollerBCX(RollerBCXBase):

    def __init__(self, name, axes='global'):
        super(RollerBCX, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class RollerBCY(RollerBCYBase):

    def __init__(self, name, axes='global'):
        super(RollerBCY, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class RollerBCZ(RollerBCZBase):

    def __init__(self, name, axes='global'):
        super(RollerBCZ, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class RollerBCXY(RollerBCXYBase):

    def __init__(self, name, axes='global'):
        super(RollerBCXY, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class RollerBCYZ(RollerBCYZBase):

    def __init__(self, name, axes='global'):
        super(RollerBCYZ, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class RollerBCXZ(RollerBCXZBase):

    def __init__(self, name, axes='global'):
        super(RollerBCXZ, self).__init__(name, axes)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)
