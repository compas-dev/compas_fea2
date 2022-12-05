from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import Model


class OpenseesModel(Model):
    """ OpenSees implementation of the :class::`Model`.

    For detailed information about OpenSees and its API visti: https://opensees.github.io/OpenSeesDocumentation/user/interpreters.html

    Warning
    -------
    Work in Progress!

    """
    __doc__ += Model.__doc__


    def __init__(self, name=None, description=None, author=None, **kwargs):
        super(OpenseesModel, self).__init__(name=name, description=description, author=author, **kwargs)


    def _generate_jobdata(self):
        data = [f'#\nwipe\n#']
        for part in self.parts:
            data.append(part._generate_jobdata(self.bcs))
        return '\n'.join(data)
