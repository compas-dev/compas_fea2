from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.backends._core import GeneralDisplacementBase
from compas_fea2.backends._core import FixedDisplacementBase
from compas_fea2.backends._core import PinnedDisplacementBase
from compas_fea2.backends._core import FixedDisplacementXXBase
from compas_fea2.backends._core import FixedDisplacementYYBase
from compas_fea2.backends._core import FixedDisplacementZZBase
from compas_fea2.backends._core import RollerDisplacementXBase
from compas_fea2.backends._core import RollerDisplacementYBase
from compas_fea2.backends._core import RollerDisplacementZBase
from compas_fea2.backends._core import RollerDisplacementXYBase
from compas_fea2.backends._core import RollerDisplacementYZBase
from compas_fea2.backends._core import RollerDisplacementXZBase

# Author(s): Francesco Ranaudo (github.com/franaudo)


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
    line = """** Name: {} Type: Displacement/Rotation
*Boundary""".format(obj.name)
    data_section.append(line)
    c=1
    for dof in dofs:
        if dof in obj.components.keys() and obj.components[dof]!=None:
            if not obj.components[dof]:
                line = """{}, {}, {}""".format(obj.bset.name, c, c)
            else:
                line = """{}, {}, {}, {}""".format(obj.bset.name, c, c, obj.components[dof])
            data_section.append(line)
        c+=1
    return '\n'.join(data_section) +'\n'


class GeneralDisplacement(GeneralDisplacementBase):

    def __init__(self, name, bset, x=None, y=None, z=None, xx=None, yy=None, zz=None, axes='global'):
        super(GeneralDisplacement, self).__init__(name, None, x, y, z, xx, yy, zz, axes)
        self.bset = bset
        self.data = _generate_data(self)


class FixedDisplacement(FixedDisplacementBase):

    def __init__(self, name, bset, axes='global'):
        super(FixedDisplacement, self).__init__(name, None, axes)
        self.bset = bset
        self.data = _generate_data(self)


class PinnedDisplacement(PinnedDisplacementBase):

    def __init__(self, name, bset, axes='global'):
        super(PinnedDisplacement, self).__init__(name, None, axes)
        self.bset = bset
        self.data = _generate_data(self)


class FixedDisplacementXX(FixedDisplacementXXBase):

    def __init__(self, name, bset, axes='global'):
        super(FixedDisplacementXX, self).__init__(name, None, axes)
        self.bset = bset
        self.data = _generate_data(self)


class FixedDisplacementYY(FixedDisplacementYYBase):

    def __init__(self, name, bset, axes='global'):
        super(FixedDisplacementYY, self).__init__(name, None, axes)
        self.bset = bset
        self.data = _generate_data(self)


class FixedDisplacementZZ(FixedDisplacementZZBase):

    def __init__(self, name, bset, axes='global'):
        super(FixedDisplacementZZ, self).__init__(name, None, axes)
        self.bset = bset
        self.data = _generate_data(self)


class RollerDisplacementX(RollerDisplacementXBase):

    def __init__(self, name, bset, axes='global'):
        super(RollerDisplacementX, self).__init__(name, None, axes)
        self.bset = bset
        self.data = _generate_data(self)


class RollerDisplacementY(RollerDisplacementYBase):

    def __init__(self, name, bset, axes='global'):
        super(RollerDisplacementY, self).__init__(name, None, axes)
        self.bset = bset
        self.data = _generate_data(self)


class RollerDisplacementZ(RollerDisplacementZBase):

    def __init__(self, name, bset, axes='global'):
        super(RollerDisplacementZ, self).__init__(name, None, axes)
        self.bset = bset
        self.data = _generate_data(self)


class RollerDisplacementXY(RollerDisplacementXYBase):

    def __init__(self, name, bset, axes='global'):
        super(RollerDisplacementXY, self).__init__(name, None, axes)
        self.bset = bset
        self.data = _generate_data(self)


class RollerDisplacementYZ(RollerDisplacementYZBase):

    def __init__(self, name, bset, axes='global'):
        super(RollerDisplacementYZ, self).__init__(name, None, axes)
        self.bset = bset
        self.data = _generate_data(self)


class RollerDisplacementXZ(RollerDisplacementXZBase):

    def __init__(self, name, bset, axes='global'):
        super(RollerDisplacementXZ, self).__init__(name, None, axes)
        self.bset = bset
        self.data = _generate_data(self)


if __name__ == "__main__":
    d = RollerDisplacementXZ('test_disp', 'test set')
    print(d.data)
    # f=open('C:/temp/test_input.inp','w')
    # # d.write_keyword(f)
    # d.write_data(f)
    # f.close()


