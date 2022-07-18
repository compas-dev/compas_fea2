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
    __doc__ += """
    Additional Parameters
    ---------------------
    ndm : int
        Dimensionality of the model. Can be from 1, 2, or 3 3, by default
        3 (3d model).
    ndof : int
        number of degree of freedom at the nodes. Can be from 1 to 6, by default
        6 (3d model).

    """

    def __init__(self, name=None, description=None, ndm=3, author=None, **kwargs):
        super(OpenseesModel, self).__init__(name=name, description=description, author=author, **kwargs)
        self._ndm = ndm
        self._ndf = {1: 1, 2: 3, 3: 6}[self._ndm]

    @property
    def ndm(self):
        """The ndm property."""
        return self._ndm

    @ndm.setter
    def ndm(self, value):
        value = int(value)
        if value < 1 or value > 3:
            raise ValueError('The model dimension can be either 1,2 or 3.')
        self._ndm = value
        self._ndf = {1: 1, 2: 3, 3: 6}[self._ndm]

    @property
    def ndf(self):
        return self._ndf

    def _generate_jobdata(self):
        if len(self._parts) > 1:
            raise NotImplementedError('Currently multiple parts are not supported in OpenSees')
        # part_name = list(self._parts)[0]
        return """#
#
wipe
model Basic -ndm {} -ndf {}
#
#
#------------------------------------------------------------------
# Nodes
#------------------------------------------------------------------
#
#    tag        X       Y       Z       mx      my      mz
{}
#
#
#
#------------------------------------------------------------------
# Materials
#------------------------------------------------------------------
#
{}
#
#
#
#------------------------------------------------------------------
# Sections
#------------------------------------------------------------------
#
{}
#
#
#
#------------------------------------------------------------------
# Elements
#------------------------------------------------------------------
#
{}
#
#
#------------------------------------------------------------------
# Initial conditions
#------------------------------------------------------------------
#
#    tag   DX   DY   RZ   MX   MY   MZ
{}
#
#
""".format(self._ndm,
           self._ndf,
           self._generate_nodes_data(),
           self._generate_materials_data(),
           self._generate_sections_data(),
           self._generate_elements_data(),
           self._generate_bc_data(),
           )

    def _generate_nodes_data(self):
        part = list(self._parts)[0]
        return '\n'.join([node._generate_jobdata() for node in part.nodes])

    def _generate_elements_data(self):
        part = list(self._parts)[0]
        return '\n'.join([element._generate_jobdata() for element in part._elements])

    def _generate_materials_data(self):
        part = list(self._parts)[0]
        return '\n'.join([material._generate_jobdata(i) for i, material in enumerate(part.materials)])

    def _generate_sections_data(self):
        part = list(self._parts)[0]
        return '\n'.join([section._generate_jobdata() for section in part.sections])

    def _generate_bc_data(self):
        part = list(self.parts)[0]
        bc_nodes = self.bcs[part]
        return '\n'.join([bc._generate_jobdata(nodes) for bc, nodes in bc_nodes.items()])
