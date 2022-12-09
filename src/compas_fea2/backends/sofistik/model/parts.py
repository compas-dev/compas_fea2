from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.parts import DeformablePart
from compas_fea2.model.parts import RigidPart

class SofistikDeformablePart(DeformablePart):
    """Sofistik implementation of :class:`compas_fea2.model.parts.DeformablePart`.\n
    """
    __doc__ += DeformablePart.__doc__

    def __init__(self, name=None, **kwargs):
        super(SofistikDeformablePart, self).__init__(name=name, **kwargs)

    def _generate_jobdata(self):
        return """$
+prog aqua urs:1
head Design Code and Materials


$ MATERIALS
{}
$ mat no 10  e 200000  mue 0.3

$ SECTIONS
{}
srec no 10  h 1000[mm]  b 100[mm]  mno 10
end

+prog SOFIMSHA urs:5
head Geometry
syst spac  gdir negz  gdiv 10000
$ NODES
{}

$ ELEMENTS
{}

end
""".format("\n".join([material._generate_jobdata() for material in self.materials]),
            "\n".join([section._generate_jobdata() for section in self.sections]), 
            "\n".join([node._generate_jobdata() for node in self.nodes]), 
            "\n".join([element._generate_jobdata() for element in self.elements])
            )


class SofistikRigidPart(RigidPart):
    """Sofistik implementation of :class:`compas_fea2.model.parts.RigidPart`.\n
    """
    __doc__ += RigidPart.__doc__

    def __init__(self, reference_point=None, name=None, **kwargs):
        super(SofistikRigidPart, self).__init__(reference_point=reference_point, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

