from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class Group(FEAData):
    """Base class for all groups.
    """

    def __init__(self, **kwargs):
        super(Group, self).__init__(**kwargs)


class NodesGroup(Group):
    """Base class for all node groups.

    Parameters
    ----------
    nodes : list[:class:`compas_fea2.model.Node`]
        The nodes belonging to the group.

    Attributes
    ----------
    nodes : list[:class:`compas_fea2.model.Node`]
        The nodes belonging to the group.

    """

    def __init__(self, *, nodes, **kwargs):
        super(NodesGroup, self).__init__(**kwargs)
        self.nodes = nodes


class ElementsGroup(Group):
    """Base class for all element groups.

    Parameters
    ----------
    elements : list[:class:`compas_fea2.model.Element`]
        The elements belonging to the group.

    Attributes
    ----------
    elements : list[:class:`compas_fea2.model.Element`]
        The elements belonging to the group.

    """

    def __init__(self, *, elements, **kwargs):
        super(ElementsGroup, self).__init__(**kwargs)
        self.elements = elements


class PartsGroup(Group):
    """Base class for all element groups.

    Parameters
    ----------
    parts : list[:class:`compas_fea2.model.Part`]
        The parts belonging to the group.

    Attributes
    ----------
    parts : list[:class:`compas_fea2.model.Part`]
        The parts belonging to the group.

    """

    def __init__(self, *, parts, **kwargs):
        super(PartsGroup, self).__init__(**kwargs)
        self.parts = parts
