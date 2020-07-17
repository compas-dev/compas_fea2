from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import pickle

# from compas.geometry import centroid_points
# from compas.utilities import geometric_key

# from compas_fea2.utilities import group_keys_by_attribute
# from compas_fea2.utilities import group_keys_by_attributes

# from compas_fea2.backends._base.components.elements import *

# from compas_fea2.backends._base.components.nodes import NodeBase
# from compas_fea2.backends._base.components.properties import ElementPropertiesBase
# from compas_fea2.backends._base.components.loads import LoadBase
# from compas_fea2.backends._base.components.loads import ThermalLoadBase
# from compas_fea2.backends._base.components.bcs import GeneralDisplacementBase
# from compas_fea2.backends._base.components.materials import MaterialBase
# from compas_fea2.backends._base.components.sections import SectionBase
# from compas_fea2.backends._base.components.steps import StepBase


__all__ = [
    'ProblemBase',
]

class ProblemBase(object):
    """Initialises the Problem object.

    Parameters
    ----------
    name : str
        Name of the Structure.
    model : obj
        model object.

    Attributes
    ----------
    name : str
        Name of the Structure.
    parts : list
        List of the parts in the model.
    model : obj
        model object.
    bc : list
        List containing the boundary conditions objects.
    interactions : list
        List containing the interaction objects.
    steps : list
        List containing the Steps objects.

    """

    def __init__(self, name, model):
        self.name                 = name
        self.model              = model

        self.bcs                = {}
        self.loads              = {}
        self.displacements      = {}
        self.steps              = []
        self.steps_order        = []
        self.field_outputs      = {}
        self.history_outputs    = {}

    def __str__(self):
        data = [self.bcs,
                self.loads,
                self.displacements,
                self.steps,
                self.steps_order,
                self.field_outputs,
                self.history_outputs]
        d = []
        for entry in data:
            if entry:
                d.append('\n'.join(['  {0} : {1}'.format(i, j.__name__) for i, j in entry.items()]))
            else:
                d.append('n/a')
        return """
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
compas_fea Problem: {}
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Boundary Conditions
-------------------
{}

Loads
-----
{}

Steps
-----
{}

Steps Order
-----------
{}

Field Output Requests
---------------------
{}

History Output Requests
-----------------------
{}


""".format(self.name, n, m, d[0], d[1], d[2], d[3], d[4], d[5])

    # ==============================================================================
    # Nodes
    # ==============================================================================

    # def check_node_exists(self, xyz):
    #     """Check if a node already exists at given x, y, z co-ordinates.

    #     Parameters
    #     ----------
    #     xyz : list
    #         [x, y, z] co-ordinates of node to check.

    #     Returns
    #     -------
    #     int
    #         The node index if the node already exists, None if not.

    #     Notes
    #     -----
    #     Geometric key check is made according to self.tol [m] tolerance.
    #     """
    #     xyz = [float(i) for i in xyz]
    #     return self.node_index.get(geometric_key(xyz, '{0}f'.format(self.tol)), None)

    # def edit_node(self, key, attr_dict):
    #     """Edit the data of a node.

    #     Parameters
    #     ----------
    #     key : int
    #         Key of the node to edit.
    #     attr_dict : dict
    #         Attribute dictionary of data to edit.

    #     Returns
    #     -------
    #     None
    #     """
    #     gkey = geometric_key(self.node_xyz(key), '{0}f'.format(self.tol))
    #     del self.node_index[gkey]
    #     for attr, item in attr_dict.items():
    #         setattr(self.nodes[key], attr, item)
    #     self.add_node_to_node_index(key, self.node_xyz(key))

    # def node_bounds(self):
    #     """Return the bounds formed by the Structure's nodal co-ordinates.

    #     Parameters
    #     ----------
    #     None

    #     Returns
    #     -------
    #     list
    #         [xmin, xmax].
    #     list
    #         [ymin, ymax].
    #     list
    #         [zmin, zmax].
    #     """
    #     n = self.node_count()
    #     x = [0] * n
    #     y = [0] * n
    #     z = [0] * n
    #     for c, node in self.nodes.items():
    #         x[c] = node.x
    #         y[c] = node.y
    #         z[c] = node.z
    #     xmin, xmax = min(x), max(x)
    #     ymin, ymax = min(y), max(y)
    #     zmin, zmax = min(z), max(z)
    #     return [xmin, xmax], [ymin, ymax], [zmin, zmax]

    # def node_count(self):
    #     """Return the number of nodes in the Structure.

    #     Parameters
    #     ----------
    #     None

    #     Returns
    #     -------
    #     int
    #         Number of nodes stored in the Structure object.
    #     """
    #     return len(self.nodes) + len(self.virtual_nodes)


    def nodes_xyz(self, nodes=None):
        """Return the xyz co-ordinates of given or all nodes.

        Parameters
        ----------
        nodes : list
            Node numbers, give None for all nodes.

        Returns
        -------
        list
            [[x, y, z] ...] co-ordinates.
        """
        if nodes is None:
            nodes = sorted(self.nodes, key=int)

        return [self.node_xyz(node=node) for node in nodes]


    # def check_element_exists(self, nodes=None, xyz=None, virtual=False):
    #     """Check if an element already exists based on nodes or centroid.

    #     Parameters
    #     ----------
    #     nodes : list
    #         Node numbers the element is connected to.
    #     xyz : list
    #         Direct co-ordinates of the element centroid to check.
    #     virtual: bool
    #         Is the element to be checked a virtual element.

    #     Returns
    #     -------
    #     int
    #         The element index if the element already exists, None if not.

    #     Notes
    #     -----
    #     Geometric key check is made according to self.tol [m] tolerance.
    #     """
    #     if not xyz:
    #         xyz = centroid_points([self.node_xyz(node) for node in nodes])
    #     gkey = geometric_key(xyz, '{0}f'.format(self.tol))
    #     if virtual:
    #         return self.virtual_element_index.get(gkey, None)
    #     else:
    #         return self.element_index.get(gkey, None)

    # def edit_element(self):
    #     raise NotImplementedError

    # def element_count(self):
    #     """Return the number of elements in the Structure.

    #     Parameters
    #     ----------
    #     None

    #     Returns
    #     -------
    #     int
    #         Number of elements stored in the Structure object.
    #     """
    #     return len(self.elements) + len(self.virtual_elements)

    # def element_centroid(self, element):
    #     """Return the centroid of an element.

    #     Parameters
    #     ----------
    #     element : int
    #         Number of the element.

    #     Returns
    #     -------
    #     list
    #         Co-ordinates of the element centroid.
    #     """
    #     return centroid_points(self.nodes_xyz(nodes=self.elements[element].nodes))

    # def add_virtual_element(self, nodes, type, thermal=False, axes={}):
    #     """Adds a virtual element to structure.elements and to element set 'virtual_elements'.

    #     Parameters
    #     ----------
    #     nodes : list
    #         Nodes the element is connected to.
    #     type : str
    #         Element type: 'HexahedronElement', 'BeamElement, 'TrussElement' etc.
    #     thermal : bool
    #         Thermal properties on or off.
    #     axes : dict
    #         The local element axes 'ex', 'ey' and 'ez'.

    #     Returns
    #     -------
    #     int
    #         Key of the added virtual element.

    #     Notes
    #     -----
    #     Virtual elements are numbered sequentially starting from 0.
    #     """
    #     ekey = self.check_element_exists(nodes, virtual=True)

    #     if ekey is None:

    #         ekey            = self.element_count()
    #         element         = func_dict[type]()
    #         element.axes    = axes
    #         element.nodes   = nodes
    #         element.number  = ekey
    #         element.thermal = thermal

    #         self.virtual_elements[ekey] = element
    #         self.add_element_to_element_index(ekey, nodes, virtual=True)

    #         if 'virtual_elements' in self.sets:
    #             self.collections['virtual_elements']['selection'].append(ekey)
    #         else:
    #             self.collections['virtual_elements'] = {'type': 'virtual_element', 'selection': [ekey],
    #                                              'index': len(self.sets)}

    #     return ekey

    # ==============================================================================
    # Modifiers
    # ==============================================================================

    # def scale_displacements(self, displacements, factor):
    #     """Scales displacements by a given factor.

    #     Parameters
    #     ----------
    #     displacements : dict
    #         Dictionary containing the displacements to scale.
    #     factor : float
    #         Factor to scale the displacements by.

    #     Returns
    #     -------
    #     dict
    #         The scaled displacements dictionary.
    #     """
    #     disp_dic = {}

    #     for key, disp in displacements.items():
    #         for dkey, dcomp in disp.components.items():
    #             if dcomp is not None:
    #                 disp.components[dkey] *= factor
    #         disp_dic[key] = disp

    #     return disp_dic

    # def scale_loads(self, loads, factor):
    #     """Scales loads by a given factor.

    #     Parameters
    #     ----------
    #     loads : dict
    #         Dictionary containing the loads to scale.
    #     factor : float
    #         Factor to scale the loads by.

    #     Returns
    #     -------
    #     dict
    #         The scaled loads dictionary.
    #     """
    #     loads_dic = {}

    #     for key, load in loads.items():
    #         for lkey, lcomp in load.components.items():
    #             if lcomp is not None:
    #                 load.components[lkey] *= factor
    #         loads_dic[key] = load

    #     return loads_dic

    # ==============================================================================
    # Steps
    # ==============================================================================

    # def set_steps_order(self, order):
    #     """Sets the order that the Steps will be analysed.

    #     Parameters
    #     ----------
    #     order : list
    #         An ordered list of the Step names.

    #     Returns
    #     -------
    #     None
    #     """
    #     self.steps_order = order

    # ==============================================================================
    # Results
    # ==============================================================================

    # def get_nodal_results(self, step, field, nodes='all'):
    #     """Extract nodal results from self.results.

    #     Parameters
    #     ----------
    #     step : str
    #         Step to extract from.
    #     field : str
    #         Data field request.
    #     nodes : str, list
    #         Extract 'all' or a node collection/list.

    #     Returns
    #     -------
    #     dict
    #         The nodal results for the requested field.
    #     """
    #     data  = {}
    #     rdict = self.results[step]['nodal']

    #     if nodes == 'all':
    #         keys = list(self.nodes.keys())
    #     else:
    #         keys = nodes

    #     for key in keys:
    #         data[key] = rdict[field][key]

    #     return data

    # def get_element_results(self, step, field, elements='all'):
    #     """Extract element results from self.results.

    #     Parameters
    #     ----------
    #     step : str
    #         Step to extract from.
    #     field : str
    #         Data field request.
    #     elements : str, list
    #         Extract 'all' or an element collection/list.

    #     Returns
    #     -------
    #     dict
    #         The element results for the requested field.
    #     """
    #     data  = {}
    #     rdict = self.results[step]['element']

    #     if elements == 'all':
    #         keys = list(self.elements.keys())

    #     # elif isinstance(elements, str):              TODO: transfor to 'collection'
    #     #     keys = self.sets[elements].selection

    #     else:
    #         keys = elements

    #     for key in keys:
    #         data[key] = rdict[field][key]

    #     return data

    # ==============================================================================
    # Summary
    # ==============================================================================

    def summary(self):
        """Prints a summary of the Structure object.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        print(self)

    # ==============================================================================
    # Save
    # ==============================================================================

    def save_to_cfea(self, path, output=True):
        """Exports the Structure object to an .obj file through Pickle.

        Parameters
        ----------
        output : bool
            Print terminal output.

        Returns
        -------
        None
        """

        filename = '{0}{1}/{2}.cfea'.format(path, self.name, self.name)

        with open(filename, 'wb') as f:
            pickle.dump(self, f)

        if output:
            print('***** Structure saved to: {0} *****\n'.format(filename))

    # ==============================================================================
    # Load
    # ==============================================================================

    @staticmethod
    def load_from_cfea(filename, output=True):
        """Imports a Structure object from an .obj file through Pickle.

        Parameters
        ----------
        filename : str
            Path to load the Structure .obj from.
        output : bool
            Print terminal output.

        Returns
        -------
        obj
            Imported Structure object.
        """
        with open(filename, 'rb') as f:
            structure = pickle.load(f)

        if output:
            print('***** Structure loaded from: {0} *****'.format(filename))

        return structure
