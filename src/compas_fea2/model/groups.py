from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from typing import Iterable

from compas_fea2.base import FEAData

# TODO change lists to sets


class _Group(FEAData):
    """Base class for all groups.

    Parameters
    ----------
    members : set
        Set with the members belonging to the group. These can be either node,
        elements, faces or parts.

    Attributes
    ----------
    registration : :class:`compas_fea2.model.DeformablePart` | :class:`compas_fea2.model.Model`
        The parent object where the members of the Group belong.

    """

    def __init__(self, members=None, name=None, **kwargs):
        super(_Group, self).__init__(name=name, **kwargs)
        self._members = set() if not members else self._check_members(members)

    def __str__(self):
        return """
{}
{}
name            : {}
# of members    : {}
""".format(self.__class__.__name__,
           len(self.__class__.__name__) * '-',
           self.name,
           len(self._members))

    def _check_member(self, member):
        if not isinstance(self, FacesGroup):
            if member._registration != self._registration:
                raise ValueError('{} is registered to a different object'.format(member))
        return member

    def _check_members(self, members):
        if not members or not isinstance(members, Iterable):
            raise ValueError('{} must be a not empty iterable'.format(members))
        # FIXME combine in more pythonic way
        if isinstance(self, FacesGroup):
            if len(set([member.element._registration for member in members])) != 1:
                raise ValueError(
                    'At least one of the members to add is registered to a different object or not registered')
            if self._registration:
                if list(members).pop().element._registration != self._registration:
                    raise ValueError(
                        'At least one of the members to add is registered to a different object than the group')
            else:
                self._registration = list(members).pop().element._registration
        else:
            if len(set([member._registration for member in members])) != 1:
                raise ValueError(
                    'At least one of the members to add is registered to a different object or not registered')
            if self._registration:
                if list(members).pop()._registration != self._registration:
                    raise ValueError(
                        'At least one of the members to add is registered to a different object than the group')
            else:
                self._registration = list(members).pop()._registration
        return members

    def _add_member(self, member):
        self._members.add(self._check_member(member))
        return member

    def _add_members(self, members):
        self._check_members(members)
        for member in members:
            self.members.add(member)
        return members


class NodesGroup(_Group):
    """Base class nodes groups.

    Note
    ----
    NodesGroups are registered to the same :class:`compas_fea2.model.DeformablePart` as its nodes
    and can belong to only one DeformablePart.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    nodes : list[:class:`compas_fea2.model.Node`]
        The nodes belonging to the group.
    part : :class:`compas_fea2.model.DeformablePart` | :class:`compas_fea2.model.Model`, optional
        The part where the members are located, by default `None`.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    nodes : list[:class:`compas_fea2.model.Node`]
        The nodes belonging to the group.
    part : :class:`compas_fea2.model.DeformablePart`
        The part where the members are located, by default `None`.

    """

    def __init__(self, *, nodes, name=None, **kwargs):
        super(NodesGroup, self).__init__(members=nodes, name=name, **kwargs)

    @property
    def part(self):
        return self._registration

    @property
    def model(self):
        return self.part._registration

    @property
    def nodes(self):
        return self._members

    def add_node(self, node):
        return self._add_member(node)

    def add_nodes(self, nodes):
        return self._add_members(nodes)


class ElementsGroup(_Group):
    """Base class for elements groups.

    Note
    ----
    ElementsGroups are registered to the same :class:`compas_fea2.model.DeformablePart` as
    its elements and can belong to only one DeformablePart.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    elements : list[:class:`compas_fea2.model.Element`]
        The elements belonging to the group.
    part : :class:`compas_fea2.model.DeformablePart` | :class:`compas_fea2.model.Model`, optional
        The part where the members are located, by default `None`.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    elements : list[:class:`compas_fea2.model.Element`]
        The elements belonging to the group.
    part : :class:`compas_fea2.model.DeformablePart`
        The part where the members are located, by default `None`.

    """

    def __init__(self, *, elements, name=None, **kwargs):
        super(ElementsGroup, self).__init__(members=elements,  name=name, **kwargs)

    @property
    def part(self):
        return self._registration

    @property
    def model(self):
        return self.part._registration

    @property
    def elements(self):
        return self._members

    def add_element(self, element):
        return self._add_member(element)

    def add_elements(self, elements):
        return self._add_members(elements)


class FacesGroup(_Group):
    """Base class elements faces groups.

    Note
    ----
    FacesGroups are registered to the same :class:`compas_fea2.model.DeformablePart` as the
    elements of its faces.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    faces : set
        The faces of the Group.
    """

    def __init__(self, *, faces, name=None, **kwargs):
        super(FacesGroup, self).__init__(members=faces, name=name, **kwargs)

    @property
    def part(self):
        return self._registration

    @property
    def model(self):
        return self.part._registration

    @property
    def faces(self):
        return self._members

    @property
    def nodes(self):
        return [node for face in self.faces for node in face.nodes]


class PartsGroup(_Group):
    """Base class for parts groups.

    Note
    ----
    PartsGroups are registered to the same :class:`compas_fea2.model.Model` as its
    parts and can belong to only one Model.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    parts : list[:class:`compas_fea2.model.DeformablePart`]
        The parts belonging to the group.

    Attributes
    ----------
    parts : list[:class:`compas_fea2.model.DeformablePart`]
        The parts belonging to the group.

    """

    def __init__(self, *, parts, name=None, **kwargs):
        super(PartsGroup, self).__init__(members=parts, name=name,  **kwargs)

    @property
    def model(self):
        return self.part._registration

    @property
    def parts(self):
        return self._members

    def add_part(self, part):
        return self._add_member(part)

    def add_parts(self, parts):
        return self._add_members(parts)
