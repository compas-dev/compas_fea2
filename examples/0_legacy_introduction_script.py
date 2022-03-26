import compas_fea2

from compas_fea2.model import Model
from compas_fea2.model import Part
from compas_fea2.model import Node
from compas_fea2.model import ElasticIsotropic
from compas_fea2.model import CircularSection
from compas_fea2.model import ShellSection
from compas_fea2.model import BeamElement
from compas_fea2.model import ShellElement
from compas_fea2.model import RollerBCXY
from compas_fea2.model.bcs import FixedBC, PinnedBC

from compas_fea2.problem import Problem
from compas_fea2.problem import PointLoad
from compas_fea2.problem import GravityLoad
from compas_fea2.problem import FieldOutput
from compas_fea2.problem import StaticStep
from compas_fea2.problem import GeneralDisplacement

from compas_fea2.results import Results
from pathlib import Path

from compas_fea2 import TEMP

compas_fea2.set_backend('abaqus')
compas_fea2.config.VERBOSE = not True


model = Model()
mat = ElasticIsotropic(E=10*10**9, v=0.3, density=1000)
sec = CircularSection(material=mat, r=0.010)

frame = Part()

coordinates = [[0., 0., 5.], [5., -5., 0.], [5., 5., 0.], [-5., 5., 0.], [-5., -5., 0.]]
nodes = [Node(xyz=node) for node in coordinates]
for i in range(1, len(nodes)):
    frame.add_element(BeamElement(nodes=[nodes[0], nodes[i]], section=sec))
model.add_part(frame)
model.add_bcs(bc=FixedBC(), nodes=nodes[1:])

# model.add_bc(bc=fix_bc, where=nodes[1:], part=frame)
# model.add_fix_bc(name='bc_pinned', part=frame, where=[1])
# model.add_pin_bc(name='bc_pinned', part=frame, where=[2, 3])
# model.add_rollerXY_bc(name='bc_pinned', part=frame, where=[4])

# Review
# model.summary()
# model.show()


##### ----------------------------- PROBLEM ----------------------------- #####
# Create the Problem object
problem = Problem(model=model)
problem.name = 'test'

# Approach 1: Create a step and assign a gravity load
step_0 = problem.add_step(StaticStep())
step_0.add_gravity_load()

# Approach 2: Add a step and define a point load directly from Problem
step_1 = problem.add_step(StaticStep())
step_1.add_point_load(x=1000, z=-1000, node=nodes[0])

# # Define the field outputs required
# fout = FieldOutput(name='fout')
# problem.add_output(fout, step_0)

# Review
# problem.summary()
# problem.show()

# Solve the problem
# problem.write_input_file()
problem.analyse(path=Path(TEMP).joinpath('refactor'))

# ##### --------------------- POSTPROCESS RESULTS -------------------------- #####
# results = Results.from_problem(problem, fields=['u'])
# pprint(results.nodal)
