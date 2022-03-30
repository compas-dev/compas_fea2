from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import Model


class OpenseesModel(Model):
    """ OpenSees implementation of the :class::`Model`.

    Warning
    -------
    Work in Progress!

    """
    __doc__ += Model.__doc__

    def __init__(self, name=None, description=None, author=None, **kwargs):
        super(OpenseesModel, self).__init__(name=name, description=description, author=author, **kwargs)
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
{self._generate_nodes_data(part_name)}
#
#
#
#------------------------------------------------------------------
# Materials
#------------------------------------------------------------------
#
{self._generate_materials_data()}
#
#
#
#------------------------------------------------------------------
# Sections
#------------------------------------------------------------------
#
{self._generate_sections_data()}
#
#
#
#------------------------------------------------------------------
# Elements
#------------------------------------------------------------------
#
{self._generate_elements_data(part_name)}
#
#
"""

    def _generate_nodes_data(self, part_name):
        return '\n'.join([node._generate_jobdata() for node in self._nodes[part_name]])

    def _generate_elements_data(self, part_name):
        return '\n'.join([element._generate_jobdata() for element in self._elements[part_name]])

    def _generate_materials_data(self):
        return '\n'.join([material._generate_jobdata(i) for i, material in enumerate(self._materials.values())])

    def _generate_sections_data(self):
        return '\n'.join([section._generate_jobdata() for section in self._sections.values()])
