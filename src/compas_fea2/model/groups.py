from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.base import FEAData


class _Group(FEAData):
    """Base class for all groups.

    Parameters
    ----------
    members : list
        List with the members belonging to the group. These can be either node,
        elements, faces or parts.
    registration : :class:`compas_fea2.model.Part` | :class:`compas_fea2.model.Model`, optional
        The part where the members are located, by default `None`.

    Attributes
    ----------
    registration : :class:`compas_fea2.model.Part`
        The part where the members are located, by default `None`.
    """

    def __init__(self, members, registration=None, name=None, **kwargs):
        super(_Group, self).__init__(name=name, **kwargs)
        self._members = self._check_members(members)
        self._registration = registration

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

    def _check_members(self, members):
        if not members:
            raise ValueError('You cannot provide an empty list')
        if not isinstance(self, FacesGroup):
            if len(set([member.registration for member in members])) != 1:
                raise ValueError('At least one member of the group is registered to a different object')
        return members

    def add_members(self, members):
        self._check_members(members)

        if members[0].registration != self._registration:
            raise ValueError('The members are registered to a different object')
        else:
            for member in members:
                self.members.add(member)

    @property
    def registration(self):
        return self._registration


class NodesGroup(_Group):
    """Base class nodes groups.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    nodes : list[:class:`compas_fea2.model.Node`]
        The nodes belonging to the group.
    part : :class:`compas_fea2.model.Part` | :class:`compas_fea2.model.Model`, optional
        The part where the members are located, by default `None`.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    nodes : list[:class:`compas_fea2.model.Node`]
        The nodes belonging to the group.
    part : :class:`compas_fea2.model.Part`
        The part where the members are located, by default `None`.

    """

    def __init__(self, *, nodes, part=None, name=None, **kwargs):
        super(NodesGroup, self).__init__(members=nodes, registration=part, name=name, **kwargs)

    @property
    def part(self):
        return self._registration

    @part.setter
    def part(self, value):
        self._registration = value

    @property
    def nodes(self):
        return self._members


class ElementsGroup(_Group):
    """Base class for elements groups.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    elements : list[:class:`compas_fea2.model.Element`]
        The elements belonging to the group.
    part : :class:`compas_fea2.model.Part` | :class:`compas_fea2.model.Model`, optional
        The part where the members are located, by default `None`.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    elements : list[:class:`compas_fea2.model.Element`]
        The elements belonging to the group.
    part : :class:`compas_fea2.model.Part`
        The part where the members are located, by default `None`.

    """

    def __init__(self, *, elements, part=None, name=None, **kwargs):
        super(ElementsGroup, self).__init__(members=elements, registration=part,  name=name, **kwargs)

    @property
    def part(self):
        return self._registration

    @part.setter
    def part(self, value):
        self._registration = value

    @property
    def elements(self):
        return self._members


class FacesGroup(_Group):
    """Base class elements faces groups.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    part : :class:`compas_fea2.model.Part`
        Part where the elements are located
    element_face : dict
        element_key, face pairs of the elements faces creating the surface
    """

    def __init__(self, *, faces, part=None, name=None, **kwargs):
        super(FacesGroup, self).__init__(members=faces, registration=part,  name=name, **kwargs)

    @property
    def part(self):
        return self._registration

    @part.setter
    def part(self, value):
        self._registration = value

    @property
    def faces(self):
        return self._members

    @property
    def nodes(self):
        return [node for face in self.faces for node in face.nodes]


class PartsGroup(_Group):
    """Base class for parts groups.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    parts : list[:class:`compas_fea2.model.Part`]
        The parts belonging to the group.

    Attributes
    ----------
    parts : list[:class:`compas_fea2.model.Part`]
        The parts belonging to the group.

    """

    def __init__(self, *, parts, name=None, **kwargs):
        super(PartsGroup, self).__init__(memebers=parts, registration=None, name=name,  **kwargs)
        raise NotImplementedError

    @property
    def parts(self):
        return self._members
