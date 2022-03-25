from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class Group(FEAData):
    """Base class for all groups.
    """

    def __init__(self, name, **kwargs):
        super(Group, self).__init__(**kwargs)
        self.name = name


class NodesGroup(Group):
    """Base class nodes groups.

    Parameters
    ----------
    nodes : list[:class:`compas_fea2.model.Node`]
        The nodes belonging to the group.

    Attributes
    ----------
    nodes : list[:class:`compas_fea2.model.Node`]
        The nodes belonging to the group.

    """

    def __init__(self, name, *, nodes, **kwargs):
        super(NodesGroup, self).__init__(name, **kwargs)
        self.nodes = nodes


class ElementsGroup(Group):
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

    def __init__(self, name, *, elements, **kwargs):
        super(ElementsGroup, self).__init__(name, **kwargs)
        self.elements = elements


# NOTE this used to be called Surface
class FacesGroup(Group):
    """Base class elements faces groups.

    Parameters
    ----------
    part : :class:`compas_fea2.model.Part`
        Part where the elements are located
    element_face : dict
        element_key, face pairs of the elements faces creating the surface
    """

    def __init__(self, name, part, element_face, **kwargs):
        super(FacesGroup, self).__init__(name, **kwargs)
        self._part = part
        self._element_face = element_face


class PartsGroup(Group):
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

    def __init__(self, name,  *, parts, **kwargs):
        super(PartsGroup, self).__init__(name, **kwargs)
        self.parts = parts
