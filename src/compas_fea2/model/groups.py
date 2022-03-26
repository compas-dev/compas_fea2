from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class _Group(FEAData):
    """Base class for all groups.
    """

    def __init__(self, name=None, **kwargs):
        super(_Group, self).__init__(**kwargs)
        self._name = name or 'Group_'+str(id(self))


class NodesGroup(_Group):
    """Base class nodes groups.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    nodes : list[:class:`compas_fea2.model.Node`]
        The nodes belonging to the group.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    nodes : list[:class:`compas_fea2.model.Node`]
        The nodes belonging to the group.

    """

    def __init__(self, nodes, name=None, **kwargs):
        super(NodesGroup, self).__init__(name=name, **kwargs)
        self.nodes = nodes


class ElementsGroup(_Group):
    """Base class for elements groups.

    Parameters
    ----------
    elements : list[:class:`compas_fea2.model.Element`]
        The elements belonging to the group.

    Attributes
    ----------
    elements : list[:class:`compas_fea2.model.Element`]
        The elements belonging to the group.

    """

    def __init__(self, *, elements, name=None, **kwargs):
        super(ElementsGroup, self).__init__(name=name, **kwargs)
        self.elements = elements


# NOTE this used to be called Surface
class FacesGroup(_Group):
    """Base class elements faces groups.

    Parameters
    ----------
    part : :class:`compas_fea2.model.Part`
        Part where the elements are located
    element_face : dict
        element_key, face pairs of the elements faces creating the surface
    """

    def __init__(self, part, element_face, name=None, **kwargs):
        super(FacesGroup, self).__init__(name=name, **kwargs)
        self._part = part
        self._element_face = element_face


class PartsGroup(_Group):
    """Base class for parts groups.

    Parameters
    ----------
    parts : list[:class:`compas_fea2.model.Part`]
        The parts belonging to the group.

    Attributes
    ----------
    parts : list[:class:`compas_fea2.model.Part`]
        The parts belonging to the group.

    """

    def __init__(self, *, parts, name=None, **kwargs):
        super(PartsGroup, self).__init__(name=name, **kwargs)
        self.parts = parts
