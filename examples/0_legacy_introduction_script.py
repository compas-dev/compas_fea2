import compas_fea2

from compas_fea2.model import Model
from compas_fea2.model import Part
from compas_fea2.model import Node
from compas_fea2.model import ElasticIsotropic
from compas_fea2.model import CircularSection
# from compas_fea2.model import ShellSection
from compas_fea2.model import BeamElement
# from compas_fea2.model import ShellElement
# from compas_fea2.model import RollerBCXY

# from compas_fea2.problem import Problem
# from compas_fea2.problem import PointLoad
# from compas_fea2.problem import GravityLoad
# from compas_fea2.problem import FieldOutput
# from compas_fea2.problem import GeneralStaticStep
# from compas_fea2.problem import GeneralDisplacement

# from compas_fea2.results import Results

compas_fea2.set_backend('abaqus')

model = Model(name='structural_model', description='test model', author='me')
mat = ElasticIsotropic(name='mat_elastic', E=10*10**9, v=0.3, density=1000)
model.add_section(CircularSection(name='sec_circ', material=mat, r=0.010))


frame = Part(name='frame')

coordinates = [[0., 0., 5.], [5., -5., 0.], [5., 5., 0.], [-5., 5., 0.], [-5., -5., 0.]]

nodes = [Node(xyz=node) for node in coordinates]
frame.add_nodes(nodes)
for i in range(1, len(nodes)):
    frame.add_element(BeamElement(nodes=[nodes[0], nodes[i]], section='sec_circ'))
model.add_part(frame)
model.add_fix_bc(name='bc_pinned', part=frame, where=[1])
model.add_pin_bc(name='bc_pinned', part=frame, where=[2, 3])
model.add_rollerXY_bc(name='bc_pinned', part=frame, where=[4])

# Review
model.summary()
# model.show(node_labels={'part-1': [0, 1]})


# ##### ----------------------------- PROBLEM ----------------------------- #####
# # Create the Problem object
# problem = Problem(name='test_structure', model=model)

# # Approach 1: Create a step and assign a gravity load
# step_0 = GeneralStaticStep(name='step_pload_0')
# step_0.add_gravity_load()
# problem.add_step(step_0)

# # Approach 2: Add a step and define a point load directly from Problem
# problem.add_step(GeneralStaticStep(name='step_pload_1'))
# problem.add_point_load(name='load_point', x=1000, z=-1000, where=[0], part='frame', step='step_pload_1')

# # Define the field outputs required
# fout = FieldOutput(name='fout')
# problem.add_output(fout, step_0)

# # Review
# problem.summary()
# problem.show()

# # Solve the problem
# problem.analyse(path=Path(TEMP).joinpath(problem.name))

# ##### --------------------- POSTPROCESS RESULTS -------------------------- #####
# results = Results.from_problem(problem, fields=['u'])
# pprint(results.nodal)
