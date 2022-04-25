from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.constraints import Pin2DConstraint
from compas_fea2.model.constraints import Pin3DConstraint
from compas_fea2.model.constraints import SliderConstraint
from compas_fea2.model.constraints import TieConstraint

class AnsysPin2DConstraint(Pin2DConstraint):
    """ Ansys implementation of :class:`.Pin2DConstraint`.\n
    """
    __doc__ += Pin2DConstraint.__doc__

    def __init__(self, *, master, slave, tol, axis, name=None, **kwargs):
        super(AnsysPin2DConstraint, self).__init__(master=master, slave=slave, tol=tol, axis=axis, name=name, **kwargs)
        raise NotImplementedError()

    def _generate_jobdata(self):
        raise NotImplementedError()

class AnsysPin3DConstraint(Pin3DConstraint):
    """ Ansys implementation of :class:`.Pin3DConstraint`.\n
    """
    __doc__ += Pin3DConstraint.__doc__

    def __init__(self, *, master, slave, tol, name=None, **kwargs):
        super(AnsysPin3DConstraint, self).__init__(master=master, slave=slave, tol=tol, name=name, **kwargs)
        raise NotImplementedError()

    def _generate_jobdata(self):
        raise NotImplementedError()

class AnsysSliderConstraint(SliderConstraint):
    """ Ansys implementation of :class:`.SliderConstraint`.\n
    """
    __doc__ += SliderConstraint.__doc__

    def __init__(self, *, master, slave, tol, plane, name=None, **kwargs):
        super(AnsysSliderConstraint, self).__init__(master=master, slave=slave, tol=tol, plane=plane, name=name, **kwargs)
        raise NotImplementedError()

    def _generate_jobdata(self):
        raise NotImplementedError()

class AnsysTieConstraint(TieConstraint):
    """ Ansys implementation of :class:`.TieConstraint`.\n
    """
    __doc__ += TieConstraint.__doc__

    def __init__(self, *, master, slave, tol, name=None, **kwargs):
        super(AnsysTieConstraint, self).__init__(master=master, slave=slave, tol=tol, name=name, **kwargs)
        raise NotImplementedError()

    def _generate_jobdata(self):
        raise NotImplementedError()

