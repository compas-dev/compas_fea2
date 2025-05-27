import logging
from importlib import import_module
from itertools import groupby
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import Set
from typing import TypeVar

from compas_fea2.base import FEAData

# Define a generic type for members
T = TypeVar("T")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class _Group(FEAData):
    """
    Base class for all groups.

    Parameters
    ----------
    members : Iterable, optional
        An iterable containing members belonging to the group.
        Members can be nodes, elements, faces, or parts. Default is None.

    Attributes
    ----------
    _members : Set[T]
        The set of members belonging to the group.
    """

    def __init__(self, members: Iterable[T] = None, **kwargs):
        super().__init__(**kwargs)
        self._members: Set[T] = set(members) if members else set()
        self._part = None
        self._model = None

    def __len__(self) -> int:
        """Return the number of members in the group."""
        return len(self._members)

    def __contains__(self, item: T) -> bool:
        """Check if an item is in the group."""
        return item in self._members

    def __iter__(self):
        """Return an iterator over the members."""
        return iter(self._members)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {len(self._members)} members>"

    def __add__(self, other: "_Group") -> "_Group":
        """Create a new group containing all members from this group and another group."""
        if not isinstance(other, _Group):
            raise TypeError("Can only add another _Group instance.")
        return self.__class__(self._members | other._members)

    def __sub__(self, other: "_Group") -> "_Group":
        """Create a new group containing members that are in this group but not in another."""
        if not isinstance(other, _Group):
            raise TypeError("Can only subtract another _Group instance.")
        return self.__class__(self._members - other._members)

    @property
    def members(self) -> Set[T]:
        """Return the members of the group."""
        return self._members

    @property
    def sorted(self) -> List[T]:
        """
        Return the members of the group sorted in ascending order.

        Returns
        -------
        List[T]
            A sorted list of group members.
        """
        return sorted(self._members, key=lambda x: x.key)

    def sorted_by(self, key: Callable[[T], Any], reverse: bool = False) -> List[T]:
        """
        Return the members of the group sorted based on a custom key function.

        Parameters
        ----------
        key : Callable[[T], Any]
            A function that extracts a key from a member for sorting.
        reverse : bool, optional
            Whether to sort in descending order. Default is False.

        Returns
        -------
        List[T]
            A sorted list of group members based on the key function.
        """
        return sorted(self._members, key=key, reverse=reverse)

    def subgroup(self, condition: Callable[[T], bool], **kwargs) -> "_Group":
        """
        Create a subgroup based on a given condition.

        Parameters
        ----------
        condition : Callable[[T], bool]
            A function that takes a member as input and returns True if the member
            should be included in the subgroup.

        Returns
        -------
        _Group
            A new group containing the members that satisfy the condition.
        """
        filtered_members = set(filter(condition, self._members))
        return self.__class__(filtered_members, **kwargs)

    def group_by(self, key: Callable[[T], Any]) -> Dict[Any, "_Group"]:
        """
        Group members into multiple subgroups based on a key function.

        Parameters
        ----------
        key : Callable[[T], Any]
            A function that extracts a key from a member for grouping.

        Returns
        -------
        Dict[Any, _Group]
            A dictionary where keys are the grouping values and values are `_Group` instances.
        """
        sorted_members = self._members
        # try:
        #     sorted_members = sorted(self._members, key=key)
        # except TypeError:
        #     sorted_members = sorted(self._members, key=lambda x: x.key)
        grouped_members = {k: set(v) for k, v in groupby(sorted_members, key=key)}
        return {k: self.__class__(v, name=f"{self.name}") for k, v in grouped_members.items()}

    def union(self, other: "_Group") -> "_Group":
        """
        Create a new group containing all members from this group and another group.

        Parameters
        ----------
        other : _Group
            Another group whose members should be combined with this group.

        Returns
        -------
        _Group
            A new group containing all members from both groups.
        """
        if not isinstance(other, _Group):
            raise TypeError("Can only perform union with another _Group instance.")
        return self.__class__(self._members | other._members)

    def intersection(self, other: "_Group") -> "_Group":
        """
        Create a new group containing only members that are present in both groups.

        Parameters
        ----------
        other : _Group
            Another group to find common members with.

        Returns
        -------
        _Group
            A new group containing only members found in both groups.
        """
        if not isinstance(other, _Group):
            raise TypeError("Can only perform intersection with another _Group instance.")
        return self.__class__(self._members & other._members)

    def difference(self, other: "_Group") -> "_Group":
        """
        Create a new group containing members that are in this group but not in another.

        Parameters
        ----------
        other : _Group
            Another group whose members should be removed from this group.

        Returns
        -------
        _Group
            A new group containing members unique to this group.
        """
        if not isinstance(other, _Group):
            raise TypeError("Can only perform difference with another _Group instance.")
        return self.__class__(self._members - other._members)

    def add_member(self, member: T) -> None:
        """
        Add a member to the group.

        Parameters
        ----------
        member : T
            The member to add.
        """
        self._members.add(member)

    def add_members(self, members: Iterable[T]) -> None:
        """
        Add multiple members to the group.

        Parameters
        ----------
        members : Iterable[T]
            The members to add.
        """
        self._members.update(members)

    def remove_member(self, member: T) -> None:
        """
        Remove a member from the group.

        Parameters
        ----------
        member : T
            The member to remove.

        Raises
        ------
        KeyError
            If the member is not found in the group.
        """
        try:
            self._members.remove(member)
        except KeyError:
            logger.warning(f"Member {member} not found in the group.")

    def remove_members(self, members: Iterable[T]) -> None:
        """
        Remove multiple members from the group.

        Parameters
        ----------
        members : Iterable[T]
            The members to remove.
        """
        self._members.difference_update(members)

    def serialize(self) -> Dict[str, Any]:
        """
        Serialize the group to a dictionary.

        Returns
        -------
        Dict[str, Any]
            A dictionary representation of the group.
        """
        return {"members": list(self._members)}

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> "_Group":
        """
        Deserialize a dictionary to create a `_Group` instance.

        Parameters
        ----------
        data : Dict[str, Any]
            A dictionary representation of the group.

        Returns
        -------
        _Group
            A `_Group` instance with the deserialized members.
        """
        return cls(set(data.get("members", [])))

    def clear(self) -> None:
        """Remove all members from the group."""
        self._members.clear()


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
        super().__init__(members=nodes, **kwargs)

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
        return self._part

    @property
    def model(self):
        return self._model

    @property
    def nodes(self):
        return self._members

    def add_node(self, node):
        """
        Add a node to the group.

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
        """
        Add multiple nodes to the group.

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
        super().__init__(members=elements, **kwargs)

    @property
    def __data__(self):
        data = super().__data__
        data.update({"elements": [element.__data__ for element in self.elements]})
        return data

    @classmethod
    def __from_data__(cls, data):
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
        """
        Add an element to the group.

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
        """
        Add multiple elements to the group.

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

    def __init__(self, faces, **kwargs):
        super().__init__(members=faces, **kwargs)

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
        """
        Add a face to the group.

        Parameters
        ----------
        face : :class:`compas_fea2.model.Face`
            The face to add.

        Returns
        -------
        :class:`compas_fea2.model.Face`
            The face added.
        """
        return self._add_member(face)

    def add_faces(self, faces):
        """
        Add multiple faces to the group.

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
        super().__init__(members=parts, **kwargs)

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
        """
        Add a part to the group.

        Parameters
        ----------
        part : :class:`compas_fea2.model.Part`
            The part to add.

        Returns
        -------
        :class:`compas_fea2.model.Part`
            The part added.
        """
        return self._add_member(part)

    def add_parts(self, parts):
        """
        Add multiple parts to the group.

        Parameters
        ----------
        parts : [:class:`compas_fea2.model.Part`]
            The parts to add.

        Returns
        -------
        [:class:`compas_fea2.model.Part`]
            The parts added.
        """
        return self._add_members(parts)


class SectionsGroup(_Group):
    """Base class for sections groups."""

    def __init__(self, sections, **kwargs):
        super().__init__(members=sections, **kwargs)

    @property
    def sections(self):
        return self._members

    def add_section(self, section):
        return self._add_member(section)

    def add_sections(self, sections):
        return self._add_members(sections)


class MaterialsGroup(_Group):
    """Base class for materials groups."""

    def __init__(self, materials, **kwargs):
        super().__init__(members=materials, **kwargs)

    @property
    def materials(self):
        return self._members

    def add_material(self, material):
        return self._add_member(material)

    def add_materials(self, materials):
        return self._add_members(materials)


class InterfacesGroup(_Group):
    """Base class for interfaces groups."""

    def __init__(self, interfaces, **kwargs):
        super().__init__(members=interfaces, **kwargs)

    @property
    def interfaces(self):
        return self._members

    def add_interface(self, interface):
        return self._add_member(interface)

    def add_interfaces(self, interfaces):
        return self._add_members(interfaces)


class BCsGroup(_Group):
    """Base class for boundary conditions groups."""

    def __init__(self, bcs, **kwargs):
        super().__init__(members=bcs, **kwargs)

    @property
    def bcs(self):
        return self._members

    def add_bc(self, bc):
        return self._add_member(bc)

    def add_bcs(self, bcs):
        return self._add_members(bcs)


class ConnectorsGroup(_Group):
    """Base class for connectors groups."""

    def __init__(self, connectors, **kwargs):
        super().__init__(members=connectors, **kwargs)

    @property
    def connectors(self):
        return self._members

    def add_connector(self, connector):
        return self._add_member(connector)

    def add_connectors(self, connectors):
        return self._add_members(connectors)


class ConstraintsGroup(_Group):
    """Base class for constraints groups."""

    def __init__(self, constraints, **kwargs):
        super().__init__(members=constraints, **kwargs)

    @property
    def constraints(self):
        return self._members

    def add_constraint(self, constraint):
        return self._add_member(constraint)

    def add_constraints(self, constraints):
        return self._add_members(constraints)


class ICsGroup(_Group):
    """Base class for initial conditions groups."""

    def __init__(self, ics, **kwargs):
        super().__init__(members=ics, **kwargs)

    @property
    def ics(self):
        return self._members

    def add_ic(self, ic):
        return self._add_member(ic)

    def add_ics(self, ics):
        return self._add_members(ics)


class ReleasesGroup(_Group):
    """Base class for releases groups."""

    def __init__(self, releases, **kwargs):
        super().__init__(members=releases, **kwargs)

    @property
    def releases(self):
        return self._members

    def add_release(self, release):
        return self._add_member(release)

    def add_releases(self, releases):
        return self._add_members(releases)
