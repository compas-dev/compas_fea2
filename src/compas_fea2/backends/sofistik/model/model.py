from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.model import Model

class SofistikModel(Model):
    """Sofistik implementation of :class:`compas_fea2.model.model.Model`.\n
    """
    __doc__ += Model.__doc__

    def __init__(self, *, name=None, description=None, author=None, **kwargs):
        super(SofistikModel, self).__init__(name=name, description=description, author=author, **kwargs)

    def _generate_jobdata(self):
        return """$
+prog aqua urs:1
head Design Code and Materials


mat no 10  e 200000  mue 0.3
srec no 10  h 1000[mm]  b 100[mm]  mno 10

end

$ PARTS
{}

+prog sofimsha urs:2
head constraints
syst rest
ctrl rest 2

node no 1 fix pxpypzmxmymz

end
""".format("\n".join([part._generate_jobdata() for part in self.parts]),
           )


