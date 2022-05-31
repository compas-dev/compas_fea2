from copy import deepcopy
import sqlite3
from sqlite3 import Error
import compas_fea2

from compas_fea2.model import Model, elements
from compas_fea2.model import Part
from compas_fea2.model import Node
from compas_fea2.model import ElasticIsotropic, Steel
from compas_fea2.model import CircularSection, RectangularSection, MembraneSection
from compas_fea2.model import ShellSection, SolidSection
from compas_fea2.model import BeamElement, MembraneElement, ShellElement
from compas_fea2.model import RollerBCXY
from compas_fea2.model import FixedBC, PinnedBC
from compas_fea2.model import NodesGroup
from compas_fea2.model import BeamEndPinRelease

from compas_fea2.problem import Problem, displacements
from compas_fea2.problem import PointLoad
from compas_fea2.problem import GravityLoad
from compas_fea2.problem import FieldOutput
from compas_fea2.problem import StaticStep, ModalAnalysis
from compas_fea2.problem import GeneralDisplacement

from compas_fea2.results import Results
from pathlib import Path
from pprint import pprint

from compas_fea2 import TEMP

from compas_fea2.utilities._utils import _compute_model_dimensions

compas_fea2.set_backend('abaqus')
compas_fea2.config.VERBOSE = not True


model = Model()
mat = ElasticIsotropic(E=10*10**9, v=0.3, density=1000)
frame_sec = RectangularSection(w=0.05, h=0.1, material=mat)
shell_sec = ShellSection(0.02, mat)

frame = model.add_part(Part())

coordinates = [[0., 0., 5.], [5., -5., 0.], [5., 5., 0.], [-5., 5., 0.], [-5., -5., 0.]]
nodes = [Node(xyz=node, mass=10) for node in coordinates]

beam_elements = []
shell_elements = []
for i in range(1, len(nodes)):
    beam_elements.append(frame.add_element(BeamElement(nodes=[nodes[0], nodes[i]], section=frame_sec)))
    if not i == len(nodes)-1:
        shell_elements.append(frame.add_element(ShellElement(
            nodes=[nodes[0], nodes[i], nodes[i+1]], section=shell_sec)))
model.add_pin_bc(nodes=[nodes[1]])
model.add_bcs(bc=FixedBC(), nodes=nodes[2:])


print(_compute_model_dimensions(model))

# Review
model.summary()
model.show()

# ##### ----------------------------- PROBLEM ----------------------------- #####
# Create the Problem object
problem = Problem(model=model, name='test')

step_1 = problem.add_step(StaticStep())
step_1.add_point_load(x=1000, z=-1000, node=nodes[0])
fout = step_1.add_output(FieldOutput())


# Review
problem.summary()
problem.show()

# Solve the problem
problem.analyse_and_extract(path=Path(TEMP).joinpath('refactor3'))

# # # # ##### --------------------- POSTPROCESS RESULTS -------------------------- #####
problem.show(reactions=0.01)

step_1_res = problem.get_step_results(step_1)
rf = step_1_res.get_total_reactions()
print(rf)
