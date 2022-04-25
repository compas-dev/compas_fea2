import compas_fea2

from compas_fea2.backends.abaqus.model import AbaqusModel
from compas_fea2.backends.abaqus.model import AbaqusPart
from compas_fea2.backends.abaqus.model import AbaqusNode
from compas_fea2.backends.abaqus.model import AbaqusElasticIsotropic
from compas_fea2.backends.abaqus.model import AbaqusCircularSection
from compas_fea2.backends.abaqus.model import AbaqusShellSection
from compas_fea2.backends.abaqus.model import AbaqusBeamElement
from compas_fea2.backends.abaqus.model import AbaqusShellElement
from compas_fea2.backends.abaqus.model import AbaqusRollerBCXY

from compas_fea2.backends.abaqus.problem import AbaqusProblem
from compas_fea2.backends.abaqus.problem import AbaqusPointLoad
# from compas_fea2.backends.abaqus.problem import AbaqusGravityLoad
from compas_fea2.backends.abaqus.problem import AbaqusFieldOutput
from compas_fea2.backends.abaqus.problem import AbaqusStaticStep
from compas_fea2.backends.abaqus.problem import AbaqusGeneralDisplacement

from compas_fea2.results import Results
from pathlib import Path

from compas_fea2 import TEMP

compas_fea2.set_backend('abaqus')

model = AbaqusModel(name='structural_model', description='test model', author='me')
mat = AbaqusElasticIsotropic(name='mat_elastic', E=10*10**9, v=0.3, density=1000)
sec = model.add_section(AbaqusCircularSection(name='sec_circ', material=mat, r=0.010))

frame = AbaqusPart(name='frame')

print(frame)

coordinates = [[0., 0., 5.], [5., -5., 0.], [5., 5., 0.], [-5., 5., 0.], [-5., -5., 0.]]

nodes = [AbaqusNode(xyz=node) for node in coordinates]
frame.add_nodes(nodes)
for i in range(1, len(nodes)):
    frame.add_element(AbaqusBeamElement(nodes=[nodes[0], nodes[i]], section=sec))
model.add_part(frame)
model.add_fix_bc(name='bc_pinned', part=frame, where=[1])
model.add_pin_bc(name='bc_pinned', part=frame, where=[2, 3])
model.add_rollerXY_bc(name='bc_pinned', part=frame, where=[4])

# Review
model.summary()
# model.show()


##### ----------------------------- PROBLEM ----------------------------- #####
# Create the Problem object
problem = AbaqusProblem(name='test_structure', model=model)

# Approach 1: Create a step and assign a gravity load
step_0 = AbaqusStaticStep(name='step_pload_0')
step_0.add_gravity_load()
problem.add_step(step_0)

# Approach 2: Add a step and define a point load directly from Problem
step_1 = problem.add_step(AbaqusStaticStep(name='step_pload_1'))
step_1.add_point_load(name='load_point', x=1000, z=-1000, where=[0], part='frame')

# # Define the field outputs required
# fout = FieldOutput(name='fout')
# problem.add_output(fout, step_0)

# Review
problem.summary()
# problem.show()

# Solve the problem
problem.write_input_file(path=Path(TEMP).joinpath(problem.name))
# problem.analyse(path=Path(TEMP).joinpath(problem.name))

# ##### --------------------- POSTPROCESS RESULTS -------------------------- #####
# results = Results.from_problem(problem, fields=['u'])
# pprint(results.nodal)
