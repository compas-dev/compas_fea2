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
        bcs_dict = {}
        for part,bc in self.bcs.items():
            for bc_obj, nodes in bc.items():
                bcs_dict[bc_obj] = nodes
        return """$
$ PARTS
{}

$ ICs
{}

$ BCs
+prog sofimsha urs:2
head constraints
syst rest
ctrl rest 2 
{}


end
""".format(
        "\n".join([part._generate_jobdata() for part in self.parts]),
        "\n".join([ic._generate_jobdata() for ic in self.ics]),
        "\n".join([bc._generate_jobdata(nodes) for bc,nodes in bcs_dict.items()]),
           )


