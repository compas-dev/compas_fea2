import gc
import importlib
import os
import pathlib
from pathlib import Path
import pickle
from itertools import chain
from itertools import groupby

from compas.datastructures import Graph

from typing import Optional
from typing import Set
from typing import Union

from compas.geometry import Box
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import bounding_box
from compas.geometry import centroid_points
from compas.geometry import Transformation
from pint import UnitRegistry

import compas_fea2
from compas_fea2.base import FEAData
from compas_fea2.model.bcs import _BoundaryCondition
from compas_fea2.model.connectors import Connector
from compas_fea2.model.interfaces import Interface
from compas_fea2.model.constraints import _Constraint
from compas_fea2.model.elements import _Element
from compas_fea2.model.groups import ElementsGroup
from compas_fea2.model.groups import NodesGroup
from compas_fea2.model.groups import PartsGroup
from compas_fea2.model.groups import _Group
from compas_fea2.model.ics import _InitialCondition
from compas_fea2.model.materials.material import _Material
from compas_fea2.model.nodes import Node
from compas_fea2.model.parts import RigidPart
from compas_fea2.model.parts import _Part
from compas_fea2.model.sections import _Section
from compas_fea2.problem import Problem
from compas_fea2.UI import FEA2Viewer
from compas_fea2.utilities._utils import get_docstring
from compas_fea2.utilities._utils import part_method
from compas_fea2.utilities._utils import problem_method


class Model(FEAData):
    """Class representing an FEA model.

    Parameters
    ----------
    description : Optional[str], optional
        Some description of the model, by default ``None``.
        This will be added to the input file and can be useful for future reference.
    author : Optional[str], optional
        The name of the author of the model, by default ``None``.
        This will be added to the input file and can be useful for future reference.

    Attributes
    ----------
    description : Optional[str]
        Some description of the model.
    author : Optional[str]
        The name of the author of the model.
    parts : Set[:class:`compas_fea2.model.Part`]
        The parts of the model.
    bcs : dict
        Dictionary with the boundary conditions of the model and the nodes where
        these are applied.
    ics : dict
        Dictionary with the initial conditions of the model and the nodes/elements
        where these are applied.
    constraints : Set[:class:`compas_fea2.model._Constraint`]
        The constraints of the model.
    partgroups : Set[:class:`compas_fea2.model.PartsGroup`]
        The part groups of the model.
    materials : Set[:class:`compas_fea2.model.materials.Material`]
        The materials assigned in the model.
    sections : Set[:class:`compas_fea2.model._Section`]
        The sections assigned in the model.
    problems : Set[:class:`compas_fea2.problem._Problem`]
        The problems added to the model.
    path : :class:`pathlib.Path`
        Path to the main folder where the problems' results are stored.

    """

    def __init__(self, description: Optional[str] = None, author: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.description = description
        self.author = author
        self._key = 0
        self._starting_key = 0
        self._units = None
        self._path = None

        self._graph = Graph()
        self._parts: Set[_Part] = set()
        self._materials: Set[_Material] = set()
        self._sections: Set[_Section] = set()
        self._bcs = {}
        self._ics = {}
        self._interfaces: Set[Interface] = set()
        self._connectors: Set[Connector] = set()
        self._constraints: Set[_Constraint] = set()
        self._partsgroups: Set[PartsGroup] = set()
        self._problems: Set[Problem] = set()

    @property
    def __data__(self):
        return {
            "description": self.description,
            "author": self.author,
            "parts": [part.__data__ for part in self.parts],
            "bcs": {bc.__data__: [node.__data__ for node in nodes] for bc, nodes in self.bcs.items()},
            "ics": {ic.__data__: [node.__data__ for node in nodes] for ic, nodes in self.ics.items()},
            "constraints": [constraint.__data__ for constraint in self.constraints],
            "partgroups": [group.__data__ for group in self.partgroups],
            "materials": [material.__data__ for material in self.materials],
            "sections": [section.__data__ for section in self.sections],
            "problems": [problem.__data__ for problem in self.problems],
            "path": str(self.path) if self.path else None,
        }

    @classmethod
    def __from_data__(cls, data):
        """Create a Model instance from a data dictionary.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        Model
            The created Model instance.
        """
        model = cls(description=data.get("description"), author=data.get("author"))
        part_classes = {cls.__name__: cls for cls in _Part.__subclasses__()}
        for part in data.get("parts", []):
            model.add_part(part_classes[part["class"]].__from_data__(part))

        bc_classes = {cls.__name__: cls for cls in _BoundaryCondition.__subclasses__()}
        for bc_data, nodes_data in data.get("bcs", {}).items():
            model._bcs[bc_classes[bc_data["class"]].__from_data__(bc_data)] = [Node.__from_data__(node_data) for node_data in nodes_data]

        ic_classes = {cls.__name__: cls for cls in _InitialCondition.__subclasses__()}
        for ic_data, nodes_data in data.get("ics", {}).items():
            model._ics[ic_classes[ic_data["class"]].__from_data__(ic_data)] = [Node.__from_data__(node_data) for node_data in nodes_data]

        constraint_classes = {cls.__name__: cls for cls in _Constraint.__subclasses__()}
        for constraint_data in data.get("constraints", []):
            model._constraints.add(constraint_classes[constraint_data["class"]].__from_data__(constraint_data))

        group_classes = {cls.__name__: cls for cls in PartsGroup.__subclasses__()}
        for group_data in data.get("partgroups", []):
            model._partsgroups.add(group_classes[group_data["class"]].__from_data__(group_data))

        problem_classes = {cls.__name__: cls for cls in Problem.__subclasses__()}
        model._problems = {problem_classes[problem_data["class"]].__from_data__(problem_data) for problem_data in data.get("problems", [])}
        model._path = Path(data.get("path")) if data.get("path") else None
        return model

    @classmethod
    def from_template(cls, template: str, **kwargs) -> "Model":
        """Create a Model instance from a template.

        Parameters
        ----------
        template : str
            The name of the template.
        **kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        Model
            The created Model instance.

        """
        raise NotImplementedError("This function is not available yet.")
        module = importlib.import_module("compas_fea2.templates")
        template = getattr(module, template)
        return template(**kwargs)

    @property
    def parts(self) -> Set[_Part]:
        return self._parts

    @property
    def graph(self) -> Graph:
        return self._graph

    @property
    def partgroups(self) -> Set[PartsGroup]:
        return self._partsgroups

    @property
    def bcs(self) -> dict:
        return self._bcs

    @property
    def ics(self) -> dict:
        return self._ics

    @property
    def constraints(self) -> Set[_Constraint]:
        return self._constraints

    @property
    def connectors(self) -> Set[Connector]:
        return self._connectors

    @property
    def materials_dict(self) -> dict[Union[_Part, "Model"], list[_Material]]:
        materials = {part: part.materials for part in filter(lambda p: not isinstance(p, RigidPart), self.parts)}
        materials.update({self: list(self._materials)})
        return materials

    @property
    def materials(self) -> Set[_Material]:
        return set(chain(*list(self.materials_dict.values())))

    @property
    def sections_dict(self) -> dict[Union[_Part, "Model"], list[_Section]]:
        sections = {part: part.sections for part in filter(lambda p: not isinstance(p, RigidPart), self.parts)}
        sections.update({self: list(self._sections)})
        return sections

    @property
    def sections(self) -> Set[_Section]:
        return set(chain(*list(self.sections_dict.values())))

    @property
    def problems(self) -> Set[Problem]:
        return self._problems

    @property
    def loads(self) -> dict:
        return self._loads

    @property
    def path(self) -> Path:
        return self._path

    @path.setter
    def path(self, value: Union[str, Path]):
        if not isinstance(value, Path):
            try:
                value = Path(value)
            except Exception:
                raise ValueError("the path provided is not valid.")
        self._path = value.joinpath(self.name)

    @property
    def nodes_set(self) -> Set[Node]:
        node_set = set()
        for part in self.parts:
            node_set.update(part.nodes)
        return node_set

    @property
    def nodes(self) -> list[Node]:
        n = []
        for part in self.parts:
            n += list(part.nodes)
        return n

    @property
    def points(self) -> list[Point]:
        return [n.point for n in self.nodes]

    @property
    def elements(self) -> list[_Element]:
        e = []
        for part in self.parts:
            e += list(part.elements)
        return e

    @property
    def interfaces(self) -> Set[Interface]:
        return self._interfaces

    @property
    def bounding_box(self) -> Optional[Box]:
        try:
            bb = bounding_box(list(chain.from_iterable([part.bounding_box.points for part in self.parts if part.bounding_box])))
        except Exception:
            return None
        return Box.from_bounding_box(bb)

    @property
    def center(self) -> Point:
        if self.bounding_box:
            return centroid_points(self.bounding_box.points)
        else:
            return centroid_points(self.points)

    @property
    def bottom_plane(self) -> Plane:
        return Plane.from_three_points(*[self.bounding_box.points[i] for i in self.bounding_box.bottom[:3]])

    @property
    def top_plane(self) -> Plane:
        return Plane.from_three_points(*[self.bounding_box.points[i] for i in self.bounding_box.top[:3]])

    @property
    def volume(self) -> float:
        return sum(p.volume for p in self.parts)

    @property
    def units(self) -> UnitRegistry:
        return self._units

    @units.setter
    def units(self, value: UnitRegistry):
        if not isinstance(value, UnitRegistry):
            return ValueError("Pint UnitRegistry required")
        self._units = value

    def assign_keys(self, start: int = None):
        """Assign keys to the model and its parts.

        Parameters
        ----------
        start : int
            The starting key, by default None (the default starting key is used).

        Returns
        -------
        None

        """
        start = start or self._starting_key
        for i, material in enumerate(self.materials):
            material._key = i + start

        for i, section in enumerate(self.sections):
            section._key = i + start

        for i, node in enumerate(self.nodes):
            node._key = i + start

        for i, element in enumerate(self.elements):
            element._key = i + start

    # =========================================================================
    #                       Constructor methods
    # =========================================================================

    @staticmethod
    def from_cfm(path: str) -> "Model":
        """Imports a Model object from a .cfm file using Pickle.

        Parameters
        ----------
        path : str
            Complete path of the file (e.g., 'C:/temp/model.cfm').

        Returns
        -------
        :class:`compas_fea2.model.Model`
            The imported model.

        """
        with open(path, "rb") as f:
            try:
                # disable garbage collector
                gc.disable()
                model = pickle.load(f)
                # enable garbage collector again
                gc.enable()
            except Exception:
                gc.enable()
                raise RuntimeError("Model not created!")
        model.path = os.sep.join(os.path.split(path)[0].split(os.sep)[:-1])
        # check if the problems' results are stored in the same location
        for problem in model.problems:
            if not os.path.exists(os.path.join(model.path, problem.name)):
                print(f"WARNING! - Problem {problem.name} results not found! move the results folder in {model.path}")
                continue
            problem.path = os.path.join(model.path, problem.name)
            problem._db_connection = None
        return model

    # =========================================================================
    #                       De-constructor methods
    # =========================================================================

    def to_cfm(self, path: Union[str, Path]):
        """Exports the Model object to a .cfm file using Pickle.

        Parameters
        ----------
        path : Union[str, Path]
            Complete path to the new file (e.g., 'C:/temp/model.cfm').

        Returns
        -------
        None

        """
        if not isinstance(path, Path):
            path = Path(path)
        if not path.suffix == ".cfm":
            raise ValueError("Please provide a valid path including the name of the file.")
        pathlib.Path(path.parent.absolute()).mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self, f)
        print("Model saved to: {}".format(path))

    # =========================================================================
    #                             Parts methods
    # =========================================================================

    def find_part_by_name(self, name: str, casefold: bool = False) -> Optional[_Part]:
        """Find if there is a part with a given name in the model.

        Parameters
        ----------
        name : str
            The name to match
        casefold : bool, optional
            If `True` perform a case insensitive search, by default `False`.

        Returns
        -------
        :class:`compas_fea2.model.Part`

        """
        for part in self.parts:
            name_1 = part.name if not casefold else part.name.casefold()
            name_2 = name if not casefold else name.casefold()
            if name_1 == name_2:
                return part

    def contains_part(self, part: _Part) -> bool:
        """Verify that the model contains a specific part.

        Parameters
        ----------
        part : :class:`compas_fea2.model.Part`

        Returns
        -------
        bool

        """
        return part in self.parts

    def add_new_part(self, **kwargs) -> _Part:
        """Add a new Part to the Model.

        Parameters
        ----------
        name : str
            The name of the part.
        **kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        :class:`compas_fea2.model.Part`

        """
        part = _Part(**kwargs)
        return self.add_part(part)

    def add_part(self, part: _Part = None, **kwargs) -> _Part:
        """Adds a Part to the Model.

        Parameters
        ----------
        part : :class:`compas_fea2.model._Part`

        Returns
        -------
        :class:`compas_fea2.model._Part`

        Raises
        ------
        TypeError
            If the part is not a part.
        ValueError
            If a part with the same name already exists in the model.

        """
        if not part:
            if "rigig" in kwargs:
                from compas_fea2.model.parts import RigidPart

                part = RigidPart(**kwargs)
            else:
                from compas_fea2.model.parts import Part

                part = Part(**kwargs)

        if not isinstance(part, _Part):
            raise TypeError("{!r} is not a part.".format(part))

        part._registration = self
        if compas_fea2.VERBOSE:
            print("{!r} registered to {!r}.".format(part, self))

        part._key = len(self._parts)
        self._parts.add(part)
        self.graph.add_node(part, type="part")
        self.graph.add_edge(self, part, relation="contains")
        return part

    def add_parts(self, parts: list[_Part]) -> list[_Part]:
        """Add multiple parts to the model.

        Parameters
        ----------
        parts : list[:class:`compas_fea2.model.Part`]

        Returns
        -------
        list[:class:`compas_fea2.model.Part`]

        """
        return [self.add_part(part) for part in parts]

    def copy_part(self, part: _Part, transformation: Transformation) -> _Part:
        """Copy a part n times.

        Parameters
        ----------
        part : :class:`compas_fea2.model._Part`
            The part to copy.

        Returns
        -------
        :class:`compas_fea2.model._Part`
            The copied part.

        """
        new_part = part.copy()
        new_part.transform(transformation)
        return self.add_part(new_part)

    def array_parts(self, parts: list[_Part], n: int, transformation: Transformation) -> list[_Part]:
        """Array a part n times along an axis.

        Parameters
        ----------
        parts : list[:class:`compas_fea2.model.Part`]
            The part to array.
        n : int
            The number of times to array the part.
        axis : str, optional
            The axis along which to array the part, by default "x".

        Returns
        -------
        list[:class:`compas_fea2.model.Part`]
            The list of arrayed parts.

        """

        new_parts = []
        for i in range(n):
            for part in parts:
                new_part = part.copy()
                new_part.transform(transformation * i)
                new_parts.append(new_part)
        return new_parts

    # =========================================================================
    #                           Materials methods
    # =========================================================================

    def add_material(self, material: _Material) -> _Material:
        """Add a material to the model.

        Parameters
        ----------
        material : :class:`compas_fea2.model.materials.Material`

        Returns
        -------
        :class:`compas_fea2.model.materials.Material`

        """
        if not isinstance(material, _Material):
            raise TypeError("{!r} is not a material.".format(material))
        material._registration = self
        self._key = len(self._materials)
        self._materials.add(material)
        return material

    def add_materials(self, materials: list[_Material]) -> list[_Material]:
        """Add multiple materials to the model.

        Parameters
        ----------
        materials : list[:class:`compas_fea2.model.materials.Material`]

        Returns
        -------
        list[:class:`compas_fea2.model.materials.Material`]

        """
        return [self.add_material(material) for material in materials]

    def find_material_by_name(self, name: str) -> Optional[_Material]:
        """Find a material by name.

        Parameters
        ----------
        name : str
            The name of the material.

        Returns
        -------
        :class:`compas_fea2.model.materials.Material`

        """
        for material in self.materials:
            if material.name == name:
                return material

    def contains_material(self, material: _Material) -> bool:
        """Verify that the model contains a specific material.

        Parameters
        ----------
        material : :class:`compas_fea2.model.materials.Material`

        Returns
        -------
        bool

        """
        return material in self.materials

    def find_material_by_key(self, key: int) -> Optional[_Material]:
        """Find a material by key.

        Parameters
        ----------
        key : int
            The key of the material.

        Returns
        -------
        :class:`compas_fea2.model.materials.Material`

        """
        for material in self.materials:
            if material.key == key:
                return material

    def find_material_by_inputkey(self, key: int) -> Optional[_Material]:
        """Find a material by input key.

        Parameters
        ----------
        key : int
            The input key of the material.

        Returns
        -------
        :class:`compas_fea2.model.materials.Material`

        """
        for material in self.materials:
            if material.input_key == key:
                return material

    def find_materials_by_attribute(self, attr: str, value: Union[str, int, float], tolerance: float = 1) -> list[_Material]:
        """Find materials by attribute.

        Parameters
        ----------
        attr : str
            The name of the attribute.
        value : Union[str, int, float]
            The value of the attribute.
        tolerance : float, optional
            The tolerance for the search, by default 1.

        Returns
        -------
        list[:class:`compas_fea2.model.materials.Material`]

        """
        materials = []
        for material in self.materials:
            if abs(getattr(material, attr) - value) < tolerance:
                materials.append(material)
        return materials

    # =========================================================================
    #                           Sections methods
    # =========================================================================

    def add_section(self, section: _Section) -> _Section:
        """Add a section to the model.

        Parameters
        ----------
        section : :class:`compas_fea2.model.sections.Section`

        Returns
        -------
        :class:`compas_fea2.model.sections.Section`

        """
        if not isinstance(section, _Section):
            raise TypeError("{!r} is not a section.".format(section))
        self._materials.add(section.material)
        section._registration = self
        self._sections.add(section)
        return section

    def add_sections(self, sections: list[_Section]) -> list[_Section]:
        """Add multiple sections to the model.

        Parameters
        ----------
        sections : list[:class:`compas_fea2.model.sections.Section`]

        Returns
        -------
        list[:class:`compas_fea2.model.sections.Section`]

        """
        return [self.add_section(section) for section in sections]

    def find_section_by_name(self, name: str) -> Optional[_Section]:
        """Find a section by name.

        Parameters
        ----------
        name : str
            The name of the section.

        Returns
        -------
        :class:`compas_fea2.model.sections.Section`

        """
        for section in self.sections:
            if section.name == name:
                return section

    def contains_section(self, section: _Section) -> bool:
        """Verify that the model contains a specific section.

        Parameters
        ----------
        section : :class:`compas_fea2.model.sections.Section`

        Returns
        -------
        bool

        """
        return section in self.sections

    def find_section_by_key(self, key: int) -> Optional[_Section]:
        """Find a section by key.

        Parameters
        ----------
        key : int
            The key of the section.

        Returns
        -------
        :class:`compas_fea2.model.sections.Section`

        """
        for section in self.sections:
            if section.key == key:
                return section

    def find_section_by_inputkey(self, key: int) -> Optional[_Section]:
        """Find a section by input key.

        Parameters
        ----------
        key : int
            The input key of the section.

        Returns
        -------
        :class:`compas_fea2.model.sections.Section`

        """
        for section in self.sections:
            if section.input_key == key:
                return section

    def find_sections_by_attribute(self, attr: str, value: Union[str, int, float], tolerance: float = 1) -> list[_Section]:
        """Find sections by attribute.

        Parameters
        ----------
        attr : str
            The name of the attribute.
        value : Union[str, int, float]
            The value of the attribute.
        tolerance : float, optional
            The tolerance for the search, by default 1.

        Returns
        -------
        list[:class:`compas_fea2.model.sections.Section`]

        """
        sections = []
        for section in self.sections:
            if abs(getattr(section, attr) - value) < tolerance:
                sections.append(section)
        return sections

    # =========================================================================
    #                           Nodes methods
    # =========================================================================

    @get_docstring(_Part)
    @part_method
    def find_node_by_key(self, key: int) -> Node:
        pass

    @get_docstring(_Part)
    @part_method
    def find_node_by_name(self, name: str) -> Node:
        pass

    @get_docstring(_Part)
    @part_method
    def find_closest_nodes_to_node(self, node: Node, distance: float, number_of_nodes: int = 1, plane: Optional[Plane] = None) -> NodesGroup:
        pass

    @get_docstring(_Part)
    @part_method
    def find_nodes_on_plane(self, plane: Plane, tol: float = 1) -> NodesGroup:
        pass

    @get_docstring(_Part)
    @part_method
    def find_nodes_in_polygon(self, polygon: Polygon, tol: float = 1.1) -> NodesGroup:
        pass

    @get_docstring(_Part)
    @part_method
    def contains_node(self, node: Node) -> Node:
        pass

    # =========================================================================
    #                           Elements methods
    # =========================================================================

    @get_docstring(_Part)
    @part_method
    def find_element_by_key(self, key: int) -> _Element:
        pass

    @get_docstring(_Part)
    @part_method
    def find_element_by_name(self, name: str) -> _Element:
        pass

    # =========================================================================
    #                           Groups methods
    # =========================================================================

    def add_parts_group(self, group: PartsGroup) -> PartsGroup:
        """Add a PartsGroup object to the Model.

        Parameters
        ----------
        group : :class:`compas_fea2.model.PartsGroup`
            The group object to add.

        Returns
        -------
        :class:`compas_fea2.model.PartsGroup`
            The added group.

        """
        if not isinstance(group, PartsGroup):
            raise TypeError("Only PartsGroups can be added to a model")
        self.partgroups.add(group)
        group._registration = self  # FIXME wrong because the members of the group might have a different registation
        return group

    def add_parts_groups(self, groups: list[PartsGroup]) -> list[PartsGroup]:
        """Add a multiple PartsGroup object to the Model.

        Parameters
        ----------
        group : list[:class:`compas_fea2.model.PartsGroup`]
            The list with the group object to add.

        Returns
        -------
        list[:class:`compas_fea2.model.PartsGroup`]
            The list with the added groups.

        """
        return [self.add_parts_group(group) for group in groups]

    def group_parts_where(self, attr: str, value: Union[str, int, float]) -> PartsGroup:
        """Group a set of parts with a give value of a given attribute.

        Parameters
        ----------
        attr : str
            The name of the attribute.
        value : Union[str, int, float]
            The value of the attribute

        Returns
        -------
        :class:`compas_fea2.model.PartsGroup`
            The group with the matching parts.

        """
        return self.add_parts_group(PartsGroup(parts=set(filter(lambda p: getattr(p, attr) == value), self.parts)))

    # =========================================================================
    #                           BCs methods
    # =========================================================================

    def add_bcs(self, bc: _BoundaryCondition, nodes: Union[list[Node], NodesGroup], axes: str = "global") -> _BoundaryCondition:
        """Add a :class:`compas_fea2.model._BoundaryCondition` to the model.

        Parameters
        ----------
        bc : :class:`compas_fea2.model._BoundaryCondition`
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
        axes : str, optional
            Axes of the boundary condition, by default 'global'.

        Returns
        -------
        :class:`compas_fea2.model._BoundaryCondition`

        """
        if isinstance(nodes, _Group):
            nodes = nodes._members

        if isinstance(nodes, Node):
            nodes = [nodes]

        if not isinstance(bc, _BoundaryCondition):
            raise TypeError("{!r} is not a Boundary Condition.".format(bc))

        for node in nodes:
            if not isinstance(node, Node):
                raise TypeError("{!r} is not a Node.".format(node))
            if not node.part:
                raise ValueError("{!r} is not registered to any part.".format(node))
            elif node.part not in self.parts:
                raise ValueError("{!r} belongs to a part not registered to this model.".format(node))
            if isinstance(node.part, RigidPart):
                if len(nodes) != 1 or not node.is_reference:
                    raise ValueError("For rigid parts bundary conditions can be assigned only to the reference point")
            node._bc = bc

        bc._key = len(self.bcs)
        self._bcs[bc] = set(nodes)
        bc._registration = self

        return bc

    def _add_bc_type(self, bc_type: str, nodes: Union[list[Node], NodesGroup], axes: str = "global") -> _BoundaryCondition:
        """Add a :class:`compas_fea2.model.BoundaryCondition` by type.

        Parameters
        ----------
        bc_type : str
            one of the boundary condition types specified above
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'

        Notes
        -----
        The bc_type must be one of the following:

        .. csv-table::
            :header: bc_type , BC

            fix, :class:`compas_fea2.model.bcs.FixedBC`
            clampXX, :class:`compas_fea2.model.bcs.ClampBCXX`
            clampYY, :class:`compas_fea2.model.bcs.ClampBCYY`
            clampZZ, :class:`compas_fea2.model.bcs.ClampBCZZ`
            pin, :class:`compas_fea2.model.bcs.PinnedBC`
            rollerX, :class:`compas_fea2.model.bcs.RollerBCX`
            rollerY, :class:`compas_fea2.model.bcs.RollerBCY`
            rollerZ, :class:`compas_fea2.model.bcs.RollerBCZ`
            rollerXY, :class:`compas_fea2.model.bcs.RollerBCXY`
            rollerYZ, :class:`compas_fea2.model.bcs.RollerBCYZ`
            rollerXZ, :class:`compas_fea2.model.bcs.RollerBCXZ`

        """
        types = {
            "fix": "FixedBC",
            "fixXX": "FixedBCXX",
            "fixYY": "FixedBCYY",
            "fixZZ": "FixedBCZZ",
            "pin": "PinnedBC",
            "rollerX": "RollerBCX",
            "rollerY": "RollerBCY",
            "rollerZ": "RollerBCZ",
            "rollerXY": "RollerBCXY",
            "rollerYZ": "RollerBCYZ",
            "rollerXZ": "RollerBCXZ",
        }
        m = importlib.import_module("compas_fea2.model.bcs")
        bc = getattr(m, types[bc_type])()
        return self.add_bcs(bc, nodes, axes)

    def add_fix_bc(self, nodes, axes="global"):
        """Add a :class:`compas_fea2.model.FixedBC` to the nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'

        """
        return self._add_bc_type("fix", nodes, axes)

    def add_pin_bc(self, nodes, axes="global"):
        """Add a pinned boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'

        """
        return self._add_bc_type("pin", nodes, axes)

    def add_clampXX_bc(self, nodes, axes="global"):
        """Add a fixed boundary condition type free about XX to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'

        """
        return self._add_bc_type("clampXX", nodes, axes)

    def add_clampYY_bc(self, nodes, axes="global"):
        """Add a fixed boundary condition free about YY type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'

        """
        return self._add_bc_type("clampYY", nodes, axes)

    def add_clampZZ_bc(self, nodes, axes="global"):
        """Add a fixed boundary condition free about ZZ type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'

        """
        return self._add_bc_type("clampZZ", nodes, axes)

    def add_rollerX_bc(self, nodes, axes="global"):
        """Add a roller free on X boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'

        """
        return self._add_bc_type("rollerX", nodes, axes)

    def add_rollerY_bc(self, nodes, axes="global"):
        """Add a roller free on Y boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'

        """
        return self._add_bc_type("rollerY", nodes, axes)

    def add_rollerZ_bc(self, nodes, axes="global"):
        """Add a roller free on Z boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'

        """
        return self._add_bc_type("rollerZ", nodes, axes)

    def add_rollerXY_bc(self, nodes, axes="global"):
        """Add a roller free on XY boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'

        """
        return self._add_bc_type("rollerXY", nodes, axes)

    def add_rollerXZ_bc(self, nodes, axes="global"):
        """Add a roller free on XZ boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'

        """
        return self._add_bc_type("rollerXZ", nodes, axes)

    def add_rollerYZ_bc(self, nodes, axes="global"):
        """Add a roller free on YZ boundary condition type to some nodes in a part.

        Parameters
        ----------
        name : str
            name of the boundary condition
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`
            List or Group with the nodes where the boundary condition is assigned.
        axes : str, optional
            [axes of the boundary condition, by default 'global'

        """
        return self._add_bc_type("rollerYZ", nodes, axes)

    def remove_bcs(self, nodes):
        """Release a node previously restrained.

        Parameters
        ----------
        nodes : [:class:`compas_fe2.model.Node]
            List of nodes to release.

        Returns
        -------
        None

        """

        if isinstance(nodes, Node):
            nodes = [nodes]

        for node in nodes:
            if node.dof:
                self.bcs[node.dof].remove(node)
                node.dof = None
            else:
                print("WARNING: {!r} was not restrained. skipped!".format(node))

    def remove_all_bcs(self):
        """Removes all the boundary conditions from the Model.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        for _, nodes in self.bcs.items():
            self.remove_bcs(nodes)
        self.bcs = {}

    # ==============================================================================
    # Initial Conditions methods
    # ==============================================================================

    def _add_ics(self, ic, group):
        """Add a :class:`compas_fea2.model._InitialCondition` to the model.

        Parameters
        ----------
        ic : :class:`compas_fea2.model._InitialCondition`
            Initial condition object to add to the model.
        group : :class:`compas_fea2.model._Group`
            Group of Nodes/Elements where the initial condition is assigned.

        Returns
        -------
        :class:`compas_fea2.model._InitialCondition`

        """
        group.part.add_group(group)

        if not isinstance(ic, _InitialCondition):
            raise TypeError("{!r} is not a InitialCondition.".format(ic))
        for member in group.members:
            if not isinstance(member, (Node, _Element)):
                raise TypeError("{!r} is not a Node or an Element.".format(member))
            if not member.part:
                raise ValueError("{!r} is not registered to any part.".format(member))
            elif member.part not in self.parts:
                raise ValueError("{!r} belongs to a part not registered to this model.".format(member))
            member._ic = ic

        ic._key = len(self._ics)
        self._ics[ic] = group.members
        ic._registration = self

        return ic

    def add_nodes_ics(self, ic, nodes):
        """Add a :class:`compas_fea2.model._InitialCondition` to the model.

        Parameters
        ----------
        ic : :class:`compas_fea2.model._InitialCondition`
        nodes : list[:class:`compas_fea2.model.Node`] or :class:`compas_fea2.model.NodesGroup`

        Returns
        -------
        :class:`compas_fea2.model._InitialCondition`

        """
        if not isinstance(nodes, NodesGroup):
            raise TypeError("{} is not a group of nodes".format(nodes))
        self._add_ics(ic, nodes)
        return ic

    def add_elements_ics(self, ic, elements):
        """Add a :class:`compas_fea2.model._InitialCondition` to the model.

        Parameters
        ----------
        ic : :class:`compas_fea2.model._InitialCondition`
        elements : :class:`compas_fea2.model.ElementsGroup`

        Returns
        -------
        :class:`compas_fea2.model._InitialCondition`

        """
        if not isinstance(elements, ElementsGroup):
            raise TypeError("{} is not a group of elements".format(elements))
        self._add_ics(ic, elements)
        return ic

    # ==============================================================================
    # Connectors methods
    # ==============================================================================

    def add_connector(self, connector):
        """Add a :class:`compas_fea2.model.Connector` to the model.

        Parameters
        ----------
        connector : :class:`compas_fea2.model.Connector`

        Returns
        -------
        :class:`compas_fea2.model.Connector`

        """
        if not isinstance(connector, Connector):
            raise TypeError("{!r} is not a Connector.".format(connector))
        connector._key = len(self._connectors)
        self._connectors.add(connector)
        connector._registration = self

        return connector

    # ==============================================================================
    # Interfaces methods
    # ==============================================================================
    def add_interface(self, interface):
        """Add a :class:`compas_fea2.model.Interface` to the model.

        Parameters
        ----------
        interface : :class:`compas_fea2.model.Interface`
            The interface object to add to the model.

        Returns
        -------
        :class:`compas_fea2.model.Interface`

        """
        if not isinstance(interface, Interface):
            raise TypeError("{!r} is not an Interface.".format(interface))
        interface._key = len(self._interfaces)
        self._interfaces.add(interface)
        interface._registration = self

        return interface

    def add_interfaces(self, interfaces):
        """Add multiple :class:`compas_fea2.model.Interface` objects to the model.

        Parameters
        ----------
        interfaces : list[:class:`compas_fea2.model.Interface`]

        Returns
        -------
        list[:class:`compas_fea2.model.Interface`]

        """
        return [self.add_interface(interface) for interface in interfaces]

    # ==============================================================================
    # Summary
    # ==============================================================================

    def summary(self):
        """Prints a summary of the Model object.

        Returns
        -------
        str
            Model summary

        """
        parts_info = [
            "\n".join(
                [
                    "{}".format(part.name),
                    "    # of nodes: {}".format(len(part.nodes)),
                    "    # of elements: {}".format(len(part.elements)),
                    "    is_rigid : {}".format("True" if isinstance(part, RigidPart) else "False"),
                ]
            )
            for part in self.parts
        ]

        constraints_info = "\n".join([e.__repr__() for e in self.constraints])

        bc_info = []
        for bc, nodes in self.bcs.items():
            for part, part_nodes in groupby(nodes, lambda n: n.part):
                bc_info.append("{}: \n{}".format(part.name, "\n".join(["  {!r} - # of restrained nodes {}".format(bc, len(list(part_nodes)))])))
        bc_info = "\n".join(bc_info)

        ic_info = []
        for ic, nodes in self.ics.items():
            for part, part_nodes in groupby(nodes, lambda n: n.part):
                ic_info.append("{}: \n{}".format(part.name, "\n".join(["  {!r} - # of restrained nodes {}".format(ic, len(list(part_nodes)))])))
        ic_info = "\n".join(ic_info)

        data = """
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
compas_fea2 Model: {}
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

description: {}
author: {}

Parts
-----
{}

Constraints
-----------
{}

Boundary Conditions
-------------------
{}

Initial Conditions
------------------
{}
""".format(
            self.name,
            self.description or "N/A",
            self.author or "N/A",
            "\n".join(parts_info),
            constraints_info or "N/A",
            bc_info or "N/A",
            ic_info or "N/A",
        )
        print(data)
        return data

    # ==============================================================================
    # Save model file
    # ==============================================================================

    def check(self, type="quick"):
        """Check for possible problems in the model.

        Parameters
        ----------
        type : str, optional
            'quick' or 'deep' check, by default 'quick'.

        Returns
        -------
        str
            Report

        Warnings
        --------
        WIP! It is better if you check yourself...

        """

        def _check_units(self):
            """Check if the units are consistent."""
            raise NotImplementedError

        def _check_bcs(self):
            """Check if the units are consistent."""
            raise NotImplementedError

        raise NotImplementedError

    # =========================================================================
    #                       Problems methods
    # =========================================================================

    def add_problem(self, problem=None, **kwargs):
        """Add a :class:`compas_fea2.problem.Problem` object to the model.

        Parameters
        ----------
        problem : :class:`compas_fea2.problem.Problem`, optional
        kwargs : dict, optional
            Additional keyword arguments for creating a new problem.

        Returns
        -------
        :class:`compas_fea2.problem.Problem`

        Raises
        ------
        TypeError
            If problem is not of type :class:`compas_fea2.problem.Problem`.

        """
        if problem:
            if not isinstance(problem, compas_fea2.problem.Problem):
                raise TypeError("{} is not a Problem".format(problem))
        else:
            from compas_fea2.problem.problem import Problem

            problem = Problem(**kwargs)
        self._problems.add(problem)
        problem._registration = self
        return problem

    def add_problems(self, problems):
        """Add multiple :class:`compas_fea2.problem.Problem` objects to the model.

        Parameters
        ----------
        problems : list[:class:`compas_fea2.problem.Problem`]

        Returns
        -------
        list[:class:`compas_fea2.problem.Problem`]

        """
        return [self.add_problem(problem) for problem in problems]

    def find_problem_by_name(self, name):
        """Find a problem in the model using its name.

        Parameters
        ----------
        name : str

        Returns
        -------
        :class:`compas_fea2.problem.Problem`

        """
        for problem in self.problems:
            if problem.name == name:
                return problem

    # =========================================================================
    #                       Run methods
    # =========================================================================

    # @get_docstring(Problem)
    @problem_method
    def write_input_file(self, problems=None, path=None, *args, **kwargs):
        pass

    # @get_docstring(Problem)
    @problem_method
    def analyse(self, problems=None, path=None, *args, **kwargs):
        pass

    # @get_docstring(Problem)
    @problem_method
    def analyze(self, problems=None, path=None, *args, **kwargs):
        pass

    # @get_docstring(Problem)
    @problem_method
    def restart_analysis(self, problem, start, steps, **kwargs):
        pass

    # @get_docstring(Problem)
    @problem_method
    def analyse_and_extract(self, problems=None, path=None, *args, **kwargs):
        pass

    # @get_docstring(Problem)
    @problem_method
    def analyse_and_store(self, problems=None, memory_only=False, *args, **kwargs):
        raise NotImplementedError()

    # @get_docstring(Problem)
    @problem_method
    def store_results_in_model(self, problems=None, *args, **kwargs):
        raise NotImplementedError()

    # ==============================================================================
    # Results methods
    # ==============================================================================
    # @get_docstring(Problem)
    @problem_method
    def get_reaction_forces_sql(self, *, problem=None, step=None):
        pass

    # @get_docstring(Problem)
    @problem_method
    def get_reaction_moments_sql(self, problem, step=None):
        pass

    # @get_docstring(Problem)
    @problem_method
    def get_displacements_sql(self, problem, step=None):
        pass

    # @get_docstring(Problem)
    @problem_method
    def get_max_displacement_sql(self, problem, step=None, component="magnitude"):
        pass

    # @get_docstring(Problem)
    @problem_method
    def get_min_displacement_sql(self, problem, step=None, component="magnitude"):
        pass

    # @get_docstring(Problem)
    @problem_method
    def get_displacement_at_nodes_sql(self, problem, nodes, steps=None):
        pass

    @problem_method
    def get_displacement_at_point_sql(self, problem, point, steps=None):
        pass

    # ==============================================================================
    # Viewer
    # ==============================================================================

    def show(self, fast=True, scale_model=1.0, show_parts=True, show_bcs=1.0, show_loads=1.0, **kwargs):
        """Visualise the model in the viewer.

        Parameters
        ----------
        scale_model : float, optional
            Scale factor for the model, by default 1.0
        show_bcs : float, optional
            Scale factor for the boundary conditions, by default 1.0
        show_loads : float, optional
            Scale factor for the loads, by default 1.0

        """

        viewer = FEA2Viewer(center=self.center, scale_model=scale_model)
        viewer.config.vectorsize = 0.2
        viewer.add_model(self, show_parts=show_parts, opacity=0.5, show_bcs=show_bcs, show_loads=show_loads, **kwargs)
        # if show_loads:
        #     register(step.__class__, FEA2StepObject, context="Viewer")
        #     viewer.viewer.scene.add(step, step=step, scale_factor=show_loads)
        viewer.show()
        viewer.scene.clear()

    @problem_method
    def show_displacements(self, problem, *args, **kwargs):
        pass
