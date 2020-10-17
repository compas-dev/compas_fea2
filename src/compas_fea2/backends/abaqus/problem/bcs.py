from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._base.problem import GeneralDisplacementBase
from compas_fea2.backends._base.problem import FixedDisplacementBase
from compas_fea2.backends._base.problem import PinnedDisplacementBase
from compas_fea2.backends._base.problem import FixedDisplacementXXBase
from compas_fea2.backends._base.problem import FixedDisplacementYYBase
from compas_fea2.backends._base.problem import FixedDisplacementZZBase
from compas_fea2.backends._base.problem import RollerDisplacementXBase
from compas_fea2.backends._base.problem import RollerDisplacementYBase
from compas_fea2.backends._base.problem import RollerDisplacementZBase
from compas_fea2.backends._base.problem import RollerDisplacementXYBase
from compas_fea2.backends._base.problem import RollerDisplacementYZBase
from compas_fea2.backends._base.problem import RollerDisplacementXZBase

# Author(s): Francesco Ranaudo (github.com/franaudo)

#TODO: add the possibility to add bcs to nodes/elements and not only to sets

__all__ = [
    'GeneralDisplacement',
    'FixedDisplacement',
    'PinnedDisplacement',
    'FixedDisplacementXX',
    'FixedDisplacementYY',
    'FixedDisplacementZZ',
    'RollerDisplacementX',
    'RollerDisplacementY',
    'RollerDisplacementZ',
    'RollerDisplacementXY',
    'RollerDisplacementYZ',
    'RollerDisplacementXZ'
]

dofs    = ['x',  'y',  'z',  'xx', 'yy', 'zz']

def _generate_data(obj):
    data_section = []
    line = ("** Name: {} Type: Displacement/Rotation\n"
            "*Boundary").format(obj.name)
    data_section.append(line)
    c=1
    for dof in dofs:
        if dof in obj.components.keys() and obj.components[dof]!=None:
            if not obj.components[dof]:
                line = """{}, {}, {}""".format(obj.bset, c, c)
            else:
                line = """{}, {}, {}, {}""".format(obj.bset, c, c, obj.components[dof])
            data_section.append(line)
        c+=1
    return '\n'.join(data_section) +'\n'


class GeneralDisplacement(GeneralDisplacementBase):
    """Initialises the base GeneralDisplacement object.

    Parameters
    ----------
    name : str
        Name of the Displacement object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    x : float
        Value of x translation.
    y : float
        Value of y translation.
    z : float
        Value of z translation.
    xx : float
        Value of xx rotation.
    yy : float
        Value of yy rotation.
    zz : float
        Value of zz rotation.
    axes : str
        'local' or 'global' co-ordinate axes.

    Attributes
    ----------
    name : str
        Name of the Displacement object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    components : dict
        Values of x, y, z, xx, yy, zz degrees-of-freedom.
    axes : str
        'local' or 'global' coordinate axes.
    """
    def __init__(self, name, bset, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global'):
        super(GeneralDisplacement, self).__init__(name, None, x, y, z, xx, yy, zz, axes)
        self.bset = bset

    def _generate_data(self):
        return _generate_data(self)


class FixedDisplacement(FixedDisplacementBase):
    """A fixed nodal displacement boundary condition.

    Parameters
    ----------
    name : str
        Name of the RollerDisplacementXZ object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    Attributes
    ----------
    name : str
        Name of the Displacement object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    components : dict
        Values of x, y, z, xx, yy, zz degrees-of-freedom.
    axes : str
        'local' or 'global' coordinate axes.
    """
    def __init__(self, name, bset, axes='global'):
        super(FixedDisplacement, self).__init__(name, None, axes)
        self.bset = bset

    def _generate_data(self):
        return _generate_data(self)


class PinnedDisplacement(PinnedDisplacementBase):
    """A pinned nodal displacement boundary condition.

    Parameters
    ----------
    name : str
        Name of the RollerDisplacementXZ object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    Attributes
    ----------
    name : str
        Name of the Displacement object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    components : dict
        Values of x, y, z, xx, yy, zz degrees-of-freedom.
    axes : str
        'local' or 'global' coordinate axes.
    """
    def __init__(self, name, bset, axes='global'):
        super(PinnedDisplacement, self).__init__(name, None, axes)
        self.bset = bset

    def _generate_data(self):
        return _generate_data(self)


class FixedDisplacementXX(FixedDisplacementXXBase):
    """A pinned nodal displacement boundary condition clamped in XX.

    Parameters
    ----------
    name : str
        Name of the RollerDisplacementXZ object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    Attributes
    ----------
    name : str
        Name of the Displacement object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    components : dict
        Values of x, y, z, xx, yy, zz degrees-of-freedom.
    axes : str
        'local' or 'global' coordinate axes.
    """
    def __init__(self, name, bset, axes='global'):
        super(FixedDisplacementXX, self).__init__(name, None, axes)
        self.bset = bset

    def _generate_data(self):
        return _generate_data(self)


class FixedDisplacementYY(FixedDisplacementYYBase):
    """A pinned nodal displacement boundary condition clamped in YY.

    Parameters
    ----------
    name : str
        Name of the RollerDisplacementXZ object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    Attributes
    ----------
    name : str
        Name of the Displacement object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    components : dict
        Values of x, y, z, xx, yy, zz degrees-of-freedom.
    axes : str
        'local' or 'global' coordinate axes.
    """
    def __init__(self, name, bset, axes='global'):
        super(FixedDisplacementYY, self).__init__(name, None, axes)
        self.bset = bset

    def _generate_data(self):
        return _generate_data(self)


class FixedDisplacementZZ(FixedDisplacementZZBase):
    """A pinned nodal displacement boundary condition clamped in ZZ.

    Parameters
    ----------
    name : str
        Name of the RollerDisplacementXZ object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    Attributes
    ----------
    name : str
        Name of the Displacement object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    components : dict
        Values of x, y, z, xx, yy, zz degrees-of-freedom.
    axes : str
        'local' or 'global' coordinate axes.
    """
    def __init__(self, name, bset, axes='global'):
        super(FixedDisplacementZZ, self).__init__(name, None, axes)
        self.bset = bset

    def _generate_data(self):
        return _generate_data(self)


class RollerDisplacementX(RollerDisplacementXBase):
    """A pinned nodal displacement boundary condition released in X.

    Parameters
    ----------
    name : str
        Name of the RollerDisplacementXZ object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    Attributes
    ----------
    name : str
        Name of the Displacement object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    components : dict
        Values of x, y, z, xx, yy, zz degrees-of-freedom.
    axes : str
        'local' or 'global' coordinate axes.
    """
    def __init__(self, name, bset, axes='global'):
        super(RollerDisplacementX, self).__init__(name, None, axes)
        self.bset = bset

    def _generate_data(self):
        return _generate_data(self)


class RollerDisplacementY(RollerDisplacementYBase):
    """A pinned nodal displacement boundary condition released in Y.

    Parameters
    ----------
    name : str
        Name of the RollerDisplacementXZ object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    Attributes
    ----------
    name : str
        Name of the Displacement object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    components : dict
        Values of x, y, z, xx, yy, zz degrees-of-freedom.
    axes : str
        'local' or 'global' coordinate axes.
    """
    def __init__(self, name, bset, axes='global'):
        super(RollerDisplacementY, self).__init__(name, None, axes)
        self.bset = bset

    def _generate_data(self):
        return _generate_data(self)


class RollerDisplacementZ(RollerDisplacementZBase):
    """A pinned nodal displacement boundary condition released in Z.

    Parameters
    ----------
    name : str
        Name of the RollerDisplacementXZ object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    Attributes
    ----------
    name : str
        Name of the Displacement object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    components : dict
        Values of x, y, z, xx, yy, zz degrees-of-freedom.
    axes : str
        'local' or 'global' coordinate axes.
    """
    def __init__(self, name, bset, axes='global'):
        super(RollerDisplacementZ, self).__init__(name, None, axes)
        self.bset = bset

    def _generate_data(self):
        return _generate_data(self)


class RollerDisplacementXY(RollerDisplacementXYBase):
    """A pinned nodal displacement boundary condition released in X and Y.

    Parameters
    ----------
    name : str
        Name of the RollerDisplacementXZ object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    Attributes
    ----------
    name : str
        Name of the Displacement object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    components : dict
        Values of x, y, z, xx, yy, zz degrees-of-freedom.
    axes : str
        'local' or 'global' coordinate axes.
    """
    def __init__(self, name, bset, axes='global'):
        super(RollerDisplacementXY, self).__init__(name, None, axes)
        self.bset = bset

    def _generate_data(self):
        return _generate_data(self)


class RollerDisplacementYZ(RollerDisplacementYZBase):
    """A pinned nodal displacement boundary condition released in Y and Z.

    Parameters
    ----------
    name : str
        Name of the RollerDisplacementXZ object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    Attributes
    ----------
    name : str
        Name of the Displacement object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    components : dict
        Values of x, y, z, xx, yy, zz degrees-of-freedom.
    axes : str
        'local' or 'global' coordinate axes.
    """
    def __init__(self, name, bset, axes='global'):
        super(RollerDisplacementYZ, self).__init__(name, None, axes)
        self.bset = bset

    def _generate_data(self):
        return _generate_data(self)


class RollerDisplacementXZ(RollerDisplacementXZBase):
    """A pinned nodal displacement boundary condition released in X and Z.

    Parameters
    ----------
    name : str
        Name of the RollerDisplacementXZ object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    axes : str
        'local' or 'global' co-ordinate axes.

    Attributes
    ----------
    name : str
        Name of the Displacement object.
    bset : obj
        `compas_fea2` NodeSet object where the displacement is applied to.
    components : dict
        Values of x, y, z, xx, yy, zz degrees-of-freedom.
    axes : str
        'local' or 'global' coordinate axes.
    """
    def __init__(self, name, bset, axes='global'):
        super(RollerDisplacementXZ, self).__init__(name, None, axes)
        self.bset = bset

    def _generate_data(self):
        return _generate_data(self)


if __name__ == "__main__":
    d = RollerDisplacementXZ(name='bc_roller', bset='roller')
    print(d._generate_data())


