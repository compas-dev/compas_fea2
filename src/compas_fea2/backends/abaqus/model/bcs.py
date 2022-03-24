from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import FixedBC
from compas_fea2.model import PinnedBC
from compas_fea2.model import FixedBCXX
from compas_fea2.model import FixedBCYY
from compas_fea2.model import FixedBCZZ
from compas_fea2.model import RollerBCX
from compas_fea2.model import RollerBCY
from compas_fea2.model import RollerBCZ
from compas_fea2.model import RollerBCXY
from compas_fea2.model import RollerBCYZ
from compas_fea2.model import RollerBCXZ

# TODO: add the possibility to add bcs to nodes/elements and not only to sets


dofs = ['x',  'y',  'z',  'xx', 'yy', 'zz']


def _generate_jobdata(obj, instance, nodes):
    """Generates the string information for the input file.

    Note
    ----
    A node set is created during the input file generation to group the application
    point of the boundary condition. The new set name follows this name scheme:
    `_aux_{bc.name}_{instance_name}`

    Note
    ----
    Ideally, this would have not been necessary
    because it is possible to retreive nodes within the Assembly-Part definition
    by just using the format `instance_name.node_key`. However Tosca Structure
    throws an exception during the flattening of the input file (it can not run
    if the model is organised in Assembly and Parts). Below the orginal implementation
    for future reference.

    .. code-block:: python

        data_section = [f'** Name: {obj.name} Type: BC/Rotation',
                        '*Boundary, op=NEW']
        for node in nodes:
            for comp, dof in enumerate(dofs, 1):
                if dof in obj.components:
                    data_section += [f'{instance}.{node+1}, {comp}, {obj.components[dof]}']

    Parameters
    ----------
    None

    Returns
    -------
    input file data line (str).

    """
    data_section = [f'** Name: {obj.name} Type: BC/Rotation\n', '*Boundary, op=NEW']
    for node in nodes:
        for comp, dof in enumerate(dofs, 1):
            if dof in obj.components:
                data_section += [f'{instance}.{node+1}, {comp}, {obj.components[dof]}']
    return '\n'.join(data_section)


class AbaqusFixedBC(FixedBC):

    def __init__(self):
        super(AbaqusFixedBC, self).__init__()

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class AbaqusPinnedBC(PinnedBC):

    def __init__(self):
        super(AbaqusPinnedBC, self).__init__()

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class AbaqusFixedBCXX(FixedBCXX):

    def __init__(self):
        super(AbaqusFixedBCXX, self).__init__()

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class AbaqusFixedBCYY(FixedBCYY):

    def __init__(self):
        super(AbaqusFixedBCYY, self).__init__()

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class AbaqusFixedBCZZ(FixedBCZZ):

    def __init__(self):
        super(AbaqusFixedBCZZ, self).__init__()

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class AbaqusRollerBCX(RollerBCX):

    def __init__(self):
        super(AbaqusRollerBCX, self).__init__()

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class AbaqusRollerBCY(RollerBCY):

    def __init__(self):
        super(AbaqusRollerBCY, self).__init__()

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class AbaqusRollerBCZ(RollerBCZ):

    def __init__(self):
        super(AbaqusRollerBCZ, self).__init__()

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class AbaqusRollerBCXY(RollerBCXY):

    def __init__(self):
        super(AbaqusRollerBCXY, self).__init__()

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class AbaqusRollerBCYZ(RollerBCYZ):

    def __init__(self):
        super(AbaqusRollerBCYZ, self).__init__()

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class AbaqusRollerBCXZ(RollerBCXZ):

    def __init__(self):
        super(AbaqusRollerBCXZ, self).__init__()

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)
