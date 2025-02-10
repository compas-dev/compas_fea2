from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import Iterable

from compas_fea2.base import FEAData


class _Group(FEAData):
    """Base class for all groups.

    Parameters
    ----------
    members : set, optional
        Set with the members belonging to the group. These can be either node,
        elements, faces or parts. By default ``None``.

    Attributes
    ----------
    registration : :class:`compas_fea2.model.Part` | :class:`compas_fea2.model.Model`
        The parent object where the members of the Group belong.

    """

    def __init__(self, members=None, **kwargs):
        super(_Group, self).__init__(**kwargs)
        self._members = set() if not members else self._check_members(members)

    @property
    def __data__(self):
        return {
            "class": self.__class__.__base__.__name__,
        }

    @classmethod
    def __from_data__(cls, data):
        raise NotImplementedError("This method must be implemented in the subclass")

    def __str__(self):
        return """
{}
{}
name            : {}
# of members    : {}
""".format(
            self.__class__.__name__, len(self.__class__.__name__) * "-", self.name, len(self._members)
        )

    def _check_member(self, member):
        if not isinstance(self, FacesGroup):
            if member._registration != self._registration:
                raise ValueError("{} is registered to a different object".format(member))
        return member

    def _check_members(self, members):
        if not members or not isinstance(members, Iterable):
            raise ValueError("{} must be a not empty iterable".format(members))
        # FIXME combine in more pythonic way
        if isinstance(self, FacesGroup):
            if len(set([member.element._registration for member in members])) != 1:
                raise ValueError("At least one of the members to add is registered to a different object or not registered")
            if self._registration:
                if list(members).pop().element._registration != self._registration:
                    raise ValueError("At least one of the members to add is registered to a different object than the group")
            else:
                self._registration = list(members).pop().element._registration
        else:
            if len(set([member._registration for member in members])) != 1:
                raise ValueError("At least one of the members to add is registered to a different object or not registered")
            if self._registration:
                if list(members).pop()._registration != self._registration:
                    raise ValueError("At least one of the members to add is registered to a different object than the group")
            else:
                self._registration = list(members).pop()._registration
        return members

    def _add_member(self, member):
        """Add a member to the group.

        Parameters
        ----------
        member : var
            The member to add. This depends on the specific group type.

        Returns
        -------
        var
            The memeber.
        """
        self._members.add(self._check_member(member))
        return member

    def _add_members(self, members):
        """Add multiple members to the group.

        Parameters
        ----------
        members : [var]
            The members to add. These depend on the specific group type.

        Returns
        -------
        [var]
            The memebers.
        """
        self._check_members(members)
        for member in members:
            self.members.add(member)
        return members


class NodesGroup(_Group):
    """Base class nodes groups.

    Parameters
    ----------
    nodes : list[:class:`compas_fea2.model.Node`]
        The nodes belonging to the group.

    Attributes
    ----------
    nodes : list[:class:`compas_fea2.model.Node`]
        The nodes belonging to the group.
    part : :class:`compas_fea2.model._Part`
        The part where the group is registered, by default `None`.
    model : :class:`compas_fea2.model.Model`
        The model where the group is registered, by default `None`.

    Notes
    -----
    NodesGroups are registered to the same :class:`compas_fea2.model._Part` as its nodes
    and can belong to only one Part.

    """

    def __init__(self, nodes, **kwargs):
        super(NodesGroup, self).__init__(members=nodes, **kwargs)

    @property
    def __data__(self):
        data = super().__data__
        data.update({"nodes": [node.__data__ for node in self.nodes]})
        return data

    @classmethod
    def __from_data__(cls, data):
        from compas_fea2.model.nodes import Node

        return cls(nodes=[Node.__from_data__(node) for node in data["nodes"]])

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
        """Add a node to the group.

        Parameters
        ----------
        node : :class:`compas_fea2.model.Node`
            The node to add.

        Returns
        -------
        :class:`compas_fea2.model.Node`
            The node added.
        """
        return self._add_member(node)

    def add_nodes(self, nodes):
        """Add multiple nodes to the group.

        Parameters
        ----------
        nodes : [:class:`compas_fea2.model.Node`]
            The nodes to add.

        Returns
        -------
        [:class:`compas_fea2.model.Node`]
            The nodes added.
        """
        return self._add_members(nodes)


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
    part : :class:`compas_fea2.model._Part`
        The part where the group is registered, by default `None`.
    model : :class:`compas_fea2.model.Model`
        The model where the group is registered, by default `None`.

    Notes
    -----
    ElementsGroups are registered to the same :class:`compas_fea2.model.Part` as
    its elements and can belong to only one Part.

    """

    def __init__(self, elements, **kwargs):
        super(ElementsGroup, self).__init__(members=elements, **kwargs)

    @property
    def __data__(self):
        data = super().__data__
        data.update({"elements": [element.__data__ for element in self.elements]})
        return data

    @classmethod
    def __from_data__(cls, data):
        from importlib import import_module

        elements_module = import_module("compas_fea2.model.elements")
        elements = [getattr(elements_module, element_data["class"]).__from_data__(element_data) for element_data in data["elements"]]
        return cls(elements=elements)

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
        """Add an element to the group.

        Parameters
        ----------
        element : :class:`compas_fea2.model.Element`
            The element to add.

        Returns
        -------
        :class:`compas_fea2.model.Element`
            The element added.

        """
        return self._add_member(element)

    def add_elements(self, elements):
        """Add multiple elements to the group.

        Parameters
        ----------
        elements : [:class:`compas_fea2.model.Element`]
            The elements to add.

        Returns
        -------
        [:class:`compas_fea2.model.Element`]
            The elements added.

        """
        return self._add_members(elements)


class FacesGroup(_Group):
    """Base class elements faces groups.

    Parameters
    ----------
    name : str, optional
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    faces : Set[:class:`compas_fea2.model.Face`]
        The Faces belonging to the group.

    Attributes
    ----------
    name : str
        Uniqe identifier. If not provided it is automatically generated. Set a
        name if you want a more human-readable input file.
    faces : Set[:class:`compas_fea2.model.Face`]
        The Faces belonging to the group.
    nodes : Set[:class:`compas_fea2.model.Node`]
        The Nodes of the faces belonging to the group.
    part : :class:`compas_fea2.model._Part`
        The part where the group is registered, by default `None`.
    model : :class:`compas_fea2.model.Model`
        The model where the group is registered, by default `None`.

    Notes
    -----
    FacesGroups are registered to the same :class:`compas_fea2.model.Part` as the
    elements of its faces.

    """

    def __init__(self, *, faces, **kwargs):
        super(FacesGroup, self).__init__(members=faces, **kwargs)

    @property
    def __data__(self):
        data = super().__data__
        data.update({"faces": list(self.faces)})
        return data

    @classmethod
    def __from_data__(cls, data):
        obj = cls(faces=set(data["faces"]))
        obj._registration = data["registration"]
        return obj

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
        nodes_set = set()
        for face in self.faces:
            for node in face.nodes:
                nodes_set.add(node)
        return nodes_set

    def add_face(self, face):
        """Add a face to the group.

        Parameters
        ----------
        face : :class:`compas_fea2.model.Face`
            The face to add.

        Returns
        -------
        :class:`compas_fea2.model.Face`
            The element added.

        """
        return self._add_member(face)

    def add_faces(self, faces):
        """Add multiple faces to the group.

        Parameters
        ----------
        faces : [:class:`compas_fea2.model.Face`]
            The faces to add.

        Returns
        -------
        [:class:`compas_fea2.model.Face`]
            The faces added.

        """
        return self._add_members(faces)


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
    model : :class:`compas_fea2.model.Model`
        The model where the group is registered, by default `None`.

    Notes
    -----
    PartsGroups are registered to the same :class:`compas_fea2.model.Model` as its
    parts and can belong to only one Model.

    """

    def __init__(self, *, parts, **kwargs):
        super(PartsGroup, self).__init__(members=parts, **kwargs)

    @property
    def __data__(self):
        data = super().__data__
        data.update({"parts": [part.__data__ for part in self.parts]})
        return data

    @classmethod
    def __from_data__(cls, data):
        from compas_fea2.model import _Part

        part_classes = {cls.__name__: cls for cls in _Part.__subclasses__()}
        parts = [part_classes[part_data["class"]].__from_data__(part_data) for part_data in data["parts"]]
        return cls(parts=parts)

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
