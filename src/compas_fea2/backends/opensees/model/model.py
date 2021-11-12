from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Author(s): Francesco Ranaudo (github.com/franaudo)

from compas_fea2.backends._base.model import ModelBase

__all__ = [
    'Model',
]


class Model(ModelBase):
    """Initialises the Model object. This is in many aspects equivalent to an
    `Assembly` in Abaqus.
    """

    def __init__(self, name, description=None, author=None):
        super(Model, self).__init__(name, description, author)
        self._backend = 'opensees'
        self._ndof = 6

    @property
    def ndof(self):
        """The ndof property."""
        return self._ndof

    @ndof.setter
    def ndof(self, value):
        self._ndof = value

    def _generate_jobdata(self):
        if len(self._parts) > 1:
            raise NotImplementedError('Currently multiple parts are not supported in OpenSee')
        part_name = list(self._parts.keys())[0]
        nodes_jobdata = '\n'.join([node._generate_jobdata() for node in self._nodes[part_name]])
        elements_jobdata = '\n'.join([element._generate_jobdata() for element in self._elements[part_name]])
        materials_jobdata = '\n'.join([material._generate_jobdata(i)
                                       for i, material in enumerate(self._materials.values())])
        sections_jobdata = '\n'.join([section._generate_jobdata() for section in self._sections.values()])
        return f"""#
#
wipe
model basic -ndm 3 -ndf {self.ndof}
#
#
#------------------------------------------------------------------
# Nodes
#------------------------------------------------------------------
#
#    tag        X       Y       Z
{nodes_jobdata}
#
#
#
#------------------------------------------------------------------
# Materials
#------------------------------------------------------------------
#
{materials_jobdata}
#
#
#
#------------------------------------------------------------------
# Sections
#------------------------------------------------------------------
#
{sections_jobdata}
#
#
#
#------------------------------------------------------------------
# Elements
#------------------------------------------------------------------
#
{elements_jobdata}
#
#
"""


# =============================================================================
#                               Debugging
# =============================================================================
if __name__ == "__main__":
    pass
