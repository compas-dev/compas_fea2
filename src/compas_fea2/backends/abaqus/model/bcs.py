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


def _generate_jobdata(bc, instance, nodes):
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

        data_section = [f'** Name: {bc.name} Type: BC/Rotation',
                        '*Boundary, op=NEW']
        for node in nodes:
            for comp, dof in enumerate(dofs, 1):
                if dof in bc.components:
                    data_section += [f'{instance}.{node+1}, {comp}, {bc.components[dof]}']

    Parameters
    ----------
    bc : :class:`compas_fea2.model.BoundaryCondition`
        The boundary condition.
    instance : :class:`compas_fea2.backends.abaqus.model._instances._Instance`
        Instance of a part where the nodes are located.  TODO: remove -> the part is already in the nodes!
    nodes: list
        List of the node where the boundary condition is applied.

    Returns
    -------
    input file data line (str).

    """
    data_section = ['** Name: {} Type: BC/Rotation', '*Boundary, op=NEW'.format(bc.name)]
    for node in nodes:
        for comp, dof in enumerate(dofs, 1):
            if getattr(bc, dof):
                data_section += [f'{instance}.{node.key+1}, {comp}, 0']
    return '\n'.join(data_section)


class AbaqusFixedBC(FixedBC):

    def __init__(self,  name=None, **kwargs):
        super(AbaqusFixedBC, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class AbaqusPinnedBC(PinnedBC):

    def __init__(self,  name=None, **kwargs):
        super(AbaqusPinnedBC, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class AbaqusFixedBCXX(FixedBCXX):

    def __init__(self,  name=None, **kwargs):
        super(AbaqusFixedBCXX, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class AbaqusFixedBCYY(FixedBCYY):

    def __init__(self,  name=None, **kwargs):
        super(AbaqusFixedBCYY, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class AbaqusFixedBCZZ(FixedBCZZ):

    def __init__(self,  name=None, **kwargs):
        super(AbaqusFixedBCZZ, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class AbaqusRollerBCX(RollerBCX):

    def __init__(self,  name=None, **kwargs):
        super(AbaqusRollerBCX, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class AbaqusRollerBCY(RollerBCY):

    def __init__(self, name=None, **kwargs):
        super(AbaqusRollerBCY, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class AbaqusRollerBCZ(RollerBCZ):

    def __init__(self, name=None, **kwargs):
        super(AbaqusRollerBCZ, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class AbaqusRollerBCXY(RollerBCXY):

    def __init__(self, name=None, **kwargs):
        super(AbaqusRollerBCXY, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class AbaqusRollerBCYZ(RollerBCYZ):

    def __init__(self, name=None, **kwargs):
        super(AbaqusRollerBCYZ, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)


class AbaqusRollerBCXZ(RollerBCXZ):

    def __init__(self, name=None, **kwargs):
        super(AbaqusRollerBCXZ, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self, instance, nodes):
        return _generate_jobdata(self, instance, nodes)
