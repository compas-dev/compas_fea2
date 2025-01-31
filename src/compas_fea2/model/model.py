import gc
import importlib
import os
import pathlib
import pickle
from itertools import chain
from itertools import groupby
from pathlib import Path
from typing import Optional
from typing import Set
from typing import Union

from compas.geometry import Box
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import bounding_box
from compas.geometry import centroid_points
from pint import UnitRegistry

import compas_fea2
from compas_fea2 import PART_NODES_LIMIT
from compas_fea2.base import FEAData
from compas_fea2.model.bcs import _BoundaryCondition
from compas_fea2.model.connectors import Connector
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
    parts : Set[:class:`compas_fea2.model.DeformablePart`]
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
        self._parts: Set[_Part] = set()
        self._nodes = None
        self._bcs = {}
        self._ics = {}
        self._connectors: Set[Connector] = set()
        self._constraints: Set[_Constraint] = set()
        self._partsgroups: Set[PartsGroup] = set()
        self._problems: Set[Problem] = set()
        self._results = {}
        self._loads = {}
        self._path = None
        self._bounding_box = None
        self._center = None
        self._bottom_plane = None
        self._top_plane = None
        self._volume = None

    def __data__(self):
        return None

    @property
    def parts(self) -> Set[_Part]:
        return self._parts

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
    def materials(self) -> Set[_Material]:
        materials = set()
        for part in filter(lambda p: not isinstance(p, RigidPart), self.parts):
            for material in part.materials:
                materials.add(material)
        return materials

    @property
    def sections(self) -> Set[_Section]:
        sections = set()
        for part in filter(lambda p: not isinstance(p, RigidPart), self.parts):
            for section in part.sections:
                sections.add(section)
        return sections

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
    def bounding_box(self) -> Optional[Box]:
        try:
            bb = bounding_box(list(chain.from_iterable([part.bounding_box.points for part in self.parts if part.bounding_box])))
            return Box.from_bounding_box(bb)
        except Exception:
            print("WARNING: bounding box not generated")
            return None

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

    def to_json(self):
        raise NotImplementedError()

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
        :class:`compas_fea2.model.DeformablePart`

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
        part : :class:`compas_fea2.model.DeformablePart`

        Returns
        -------
        bool

        """
        return part in self.parts

    def add_part(self, part: _Part) -> _Part:
        """Adds a DeformablePart to the Model.

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
        if not isinstance(part, _Part):
            raise TypeError("{!r} is not a part.".format(part))

        if self.contains_part(part):
            if compas_fea2.VERBOSE:
                print("SKIPPED: DeformablePart {!r} is already in the model.".format(part))
            return

        if self.find_part_by_name(part.name):
            raise ValueError("Duplicate name! The name '{}' is already in use.".format(part.name))

        part._registration = self
        if compas_fea2.VERBOSE:
            print("{!r} registered to {!r}.".format(part, self))

        part._key = len(self._parts) * PART_NODES_LIMIT
        self._parts.add(part)

        if not isinstance(part, RigidPart):
            for material in part.materials:
                material._registration = self

            for section in part.sections:
                section._registration = self

        return part

    def add_parts(self, parts: list[_Part]) -> list[_Part]:
        """Add multiple parts to the model.

        Parameters
        ----------
        parts : list[:class:`compas_fea2.model.DeformablePart`]

        Returns
        -------
        list[:class:`compas_fea2.model.DeformablePart`]

        """
        return [self.add_part(part) for part in parts]

    # =========================================================================
    #                           Nodes methods
    # =========================================================================

    @get_docstring(_Part)
    @part_method
    def find_node_by_key(self, key: int):
        pass

    @get_docstring(_Part)
    @part_method
    def find_node_by_inputkey(self, input_key: int):
        pass

    @get_docstring(_Part)
    @part_method
    def find_nodes_by_name(self, name: str):
        pass

    @get_docstring(_Part)
    @part_method
    def find_nodes_around_point(self, point: Point, distance: float, plane: Optional[Plane] = None, single: bool = False):
        pass

    @get_docstring(_Part)
    @part_method
    def find_nodes_around_node(self, node: Node, distance: float):
        pass

    @get_docstring(_Part)
    @part_method
    def find_closest_nodes_to_node(self, node: Node, distance: float, number_of_nodes: int = 1, plane: Optional[Plane] = None):
        pass

    @get_docstring(_Part)
    @part_method
    def find_nodes_by_attribute(self, attr: str, value: Union[str, int, float], tolerance: float = 1):
        pass

    @get_docstring(_Part)
    @part_method
    def find_nodes_on_plane(self, plane: Plane, tolerance: float = 1):
        pass

    @get_docstring(_Part)
    @part_method
    def find_nodes_in_polygon(self, polygon: Polygon, tolerance: float = 1.1):
        pass

    @get_docstring(_Part)
    @part_method
    def find_nodes_where(self, conditions: dict):
        pass

    @get_docstring(_Part)
    @part_method
    def contains_node(self, node: Node):
        pass

    # =========================================================================
    #                           Elements methods
    # =========================================================================

    @get_docstring(_Part)
    @part_method
    def find_element_by_key(self, key: int):
        pass

    @get_docstring(_Part)
    @part_method
    def find_element_by_inputkey(self, key: int):
        pass

    @get_docstring(_Part)
    @part_method
    def find_elements_by_name(self, name: str):
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
