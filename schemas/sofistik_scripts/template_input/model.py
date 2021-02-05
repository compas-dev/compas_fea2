"""
Comments SB 03/02/2021

    - local placeholder dataclasses to represent data types

    - draft of proposal to refactor Problem class:
        Load -> LoadCase -> LoadCombination -> Analysis -> Envelope classes
        This implementation would be in line with typical FE workflow,
        allow flexible setup of multiple load cases and analyses in the same input file
        Additionally, all geometry could be grouped in Model.geometry

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import List, Dict


__all__ = [
    "Material",
    "RectangularSection",
    "Node",
    "Beam",
    "BoundaryCondition",
    "NodeLoad",
    "LoadCase",
    "LoadCombination",
    "Analysis",
    "StressInterpolation",
    "Envelope",
    "Model"
]


@dataclass
class Material:
    nr: int
    elasticity_modulus: float
    shear_ratio: float
    name: str = None

    def _generate_data(self):
        return "mat no {0:>7}  e {1:>12}  mue {2:>6}  {3}".format(
            self.nr, self.elasticity_modulus, self.shear_ratio,
            ("titl '" + self.name + "'" if self.name else ""))


@dataclass
class Section:
    def _generate_data(self):
        raise NotImplementedError

@dataclass
class RectangularSection(Section):
    nr: int
    height: float
    width: float
    material_nr: int
    name: str = None

    def _generate_data(self):
        return "srec no {0:>6}  h {1:>8}[mm]  b {2:>8}[mm]  mno {3:>6}  {4}".format(
            self.nr, self.height, self.width, self.material_nr,
            ("titl '" + self.name + "'" if self.name else ""))


@dataclass
class Node:
    nr: int
    x: float
    y: float
    z: float

    def _generate_data(self):
        return "node no {0:>8}  x {1:>12}  y {2:>12}  z {3:>12}".format(
            self.nr, self.x, self.y, self.z)


@dataclass
class Beam:
    nr: int
    start_node: int
    end_node: int
    section_nr: int
    division: int = 1
    start_hinge: str = None
    end_hinge: str = None

    def _generate_data(self):
        return "beam no {0}  na {1:>8}  ne {2:>8}  ncs {3:>8}  div {4}".format(
                self.nr, self.start_node, self.end_node, self.section_nr, self.division)


@dataclass
class BoundaryCondition:
    nr: int
    tx: bool = False
    ty: bool = False
    tz: bool = False
    rx: bool = False
    ry: bool = False
    rz: bool = False


    def _generate_data(self):
        flags = {"px" : self.tx, "py" : self.ty, "pz" : self.tz,
                "mx" : self.rx, "my" : self.ry, "mz" : self.rz}
        fixity = "".join((k if v else "") for k, v in flags.items())
        return "node no {0}  fix {1}".format(self.nr, fixity)



@dataclass
class Load:
    def _generate_data(self):
        raise NotImplementedError

@dataclass
class NodeLoad(Load):
    node_nr: int
    px: float = 0.0
    py: float = 0.0
    pz: float = 0.0

    def _generate_data(self):
        node_loads = []
        if self.px: node_loads.append("node no {0:>8}  type px  p1 {1}".format(self.node_nr, self.px))
        if self.py: node_loads.append("node no {0:>8}  type py  p1 {1}".format(self.node_nr, self.py))
        if self.pz: node_loads.append("node no {0:>8}  type pz  p1 {1}".format(self.node_nr, self.pz))
        return "\n".join(node_loads)


@dataclass
class LoadCase:
    nr: int
    loads: List[Load]
    name: str = None

    def _generate_data(self):
        load_case = "lc no {0:>7}  {1}".format(self.nr,
            ("titl '" + self.name + "'" if self.name else ""))
        loads = "\n".join(load._generate_data() for load in self.loads)
        return "\n".join((load_case, loads))


@dataclass
class LoadCombination:
    nr: int
    load_cases: List[LoadCase]
    load_case_factors: List[float] = field(default_factory=[1.0])
    dead_load_factor: float = 1.0
    name: str = None

    def _generate_data(self):
        factored_cases = ["lcc no {0:>6}  fact {1:>5}".format(lc_nr, lf)
            for lc_nr, lf in zip(list(lc.nr for lc in self.load_cases), self.load_case_factors)]
        return "\n".join(factored_cases)


@dataclass
class Analysis:
    nr: int
    load_combination: LoadCombination
    analysis_type: int = 1
    name: str = None

    # set (bit) flags for different analysis types
    # (linear, 2nd order, 3rd order, material nonl, buckling eigenvalues, dynamic eigenvalues, stress interpolation, ...)
    @property
    def analysis_types(self):
        return {0 : "syst prob line",
                1 : "syst prob th2  nmat no",
                2 : "syst prob th3  nmat no",
                5 : "syst prob th2  nmat yes",
                6 : "syst prob th3  nmat yes"}

    def _generate_data(self):
        analysis_settings = self.analysis_types[self.analysis_type]
        base_case = "lc no {0:>7}  dlz {1:>6}  {2}".format(self.nr, self.load_combination.dead_load_factor,
            ("titl '" + self.name + "'" if self.name else ""))
        factored_cases = self.load_combination._generate_data()
        return "\n".join((analysis_settings + "\n", base_case, factored_cases))


@dataclass
class StressInterpolation:
    nr: int
    analyses: List[Analysis]
    name: str = None

    def _generate_data(self):
        return "lc no {0:>7}  {1}".format(",".join(str(a.nr) for a in self.analyses),
            ("titl '" + self.name + "'" if self.name else ""))


@dataclass
class Envelope:
    nr: int
    analyses: List[Analysis]
    envelope_type: int = 1
    # set (bit) flags for different envelope types
    # (nodal displacements, internal forces, ...)

    def _generate_data(self):
        raise NotImplementedError



class Model:
    """Placeholder for model class."""
    def __init__(self, name):
        self.name = name

        self._materials = ModelData(Material)
        self._sections = ModelData(Section)

        self._nodes = ModelData(Node)
        self._beams = ModelData(Beam)
        self._boundary_conditions = ModelData(BoundaryCondition)

        self._load_cases = ModelData(LoadCase)
        self._load_combinations = ModelData(LoadCombination)
        self._analyses = ModelData(Analysis)
        self._stresses = ModelData(StressInterpolation)


    # ----- Alternative Constructors -----

    @staticmethod
    def from_database(in_file, geometry_only=False):
        raise NotImplementedError

    @staticmethod
    def from_json(in_file, geometry_only=False):
        raise NotImplementedError


    # ----- getters and setters -----

    @property
    def materials(self):
        return self._materials
    @materials.setter
    def materials(self, value):
        self._materials._dict = value._dict

    @property
    def sections(self):
        return self._sections
    @sections.setter
    def sections(self, value):
        self._sections._dict = value._dict

    @property
    def nodes(self):
        return self._nodes
    @nodes.setter
    def nodes(self, value):
        self._nodes._dict = value._dict

    @property
    def beams(self):
        return self._beams
    @beams.setter
    def beams(self, value):
        self._beams._dict = value._dict

    @property
    def boundary_conditions(self):
        return self._boundary_conditions
    @boundary_conditions.setter
    def boundary_conditions(self, value):
        self._boundary_conditions._dict = value._dict

    @property
    def load_cases(self):
        return self._load_cases
    @load_cases.setter
    def load_cases(self, value):
        self._load_cases._dict = value._dict

    @property
    def load_combinations(self):
        return self._load_combinations
    @load_combinations.setter
    def load_combinations(self, value):
        self._load_combinations._dict = value._dict

    @property
    def analyses(self):
        return self._analyses
    @analyses.setter
    def analyses(self, value):
        self._analyses._dict = value._dict

    @property
    def stresses(self):
        return self._stresses
    @stresses.setter
    def stresses(self, value):
        self._stresses._dict = value._dict



class ModelData:
    """Placeholder custom container class to internally map model data ids onto model data."""
    def __init__(self, data_type):
        self._dict = dict()
        self.data_type = data_type

    def __getitem__(self, key):
        return self._dict[key]

    def __iter__(self):
        yield from self._dict.values()

    def __add__(self, other):
        if (isinstance(other, self.__class__) and (self.data_type == other.data_type)):
            combined_data = self.__class__(self.data_type)
            combined_data._dict = {**self._dict, **other._dict}
            return combined_data
        elif isinstance(other, Iterable):
            for val in other:
                if not isinstance(val, self.data_type): continue
                self._dict[val.nr] = val
        elif isinstance(other, self.data_type):
                self._dict[other.nr] = other
        else: raise TypeError
        return self

    def __len__(self):
        return len(self._dict)
    
    def __str__(self):
        return "\n".join(str(val) for val in self._dict.values())
    
    def clear(self):
        self._dict.clear()



if __name__ == "__main__":
    pass