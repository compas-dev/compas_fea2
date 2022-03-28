import compas_fea2

from compas_fea2.model import Model, elements
from compas_fea2.model import Part
from compas_fea2.model import Node
from compas_fea2.model import ElasticIsotropic
from compas_fea2.model import CircularSection
from compas_fea2.model import ShellSection
from compas_fea2.model import BeamElement
from compas_fea2.model import ShellElement
from compas_fea2.model import RollerBCXY
from compas_fea2.model.bcs import FixedBC, PinnedBC
from compas_fea2.model import NodesGroup
from compas_fea2.model.releases import BeamEndPinRelease

from compas_fea2.problem import Problem
from compas_fea2.problem import PointLoad
from compas_fea2.problem import GravityLoad
from compas_fea2.problem import FieldOutput
from compas_fea2.problem import StaticStep
from compas_fea2.problem import GeneralDisplacement

from compas_fea2.results import Results
from pathlib import Path
from pprint import pprint

from compas_fea2 import TEMP

compas_fea2.set_backend('abaqus')
compas_fea2.config.VERBOSE = not True


model = Model()
mat = ElasticIsotropic(E=10*10**9, v=0.3, density=1000)
frame_sec = CircularSection(material=mat, r=0.010)
shell_sec = ShellSection(0.02, mat)
frame = model.add_part(Part())

coordinates = [[0., 0., 5.], [5., -5., 0.], [5., 5., 0.], [-5., 5., 0.], [-5., -5., 0.]]
nodes = [Node(xyz=node) for node in coordinates]
supports = NodesGroup(nodes[1:])
print(supports)
beam_elements = []
shell_elements = []
for i in range(1, len(nodes)):
    beam_elements.append(frame.add_element(BeamElement(nodes=[nodes[0], nodes[i]], section=frame_sec)))
    if not i == len(nodes)-1:
        shell_elements.append(frame.add_element(ShellElement(
            nodes=[nodes[0], nodes[i], nodes[i+1]], section=shell_sec)))
model.add_pin_bc(node=nodes[1])
model.add_bcs(bc=FixedBC(), nodes=nodes[2:])

pin_release = BeamEndPinRelease(m1=True)
frame.add_beam_release(element=beam_elements[0], location='start', release=pin_release)

# Review
# model.summary()
# model.show()


##### ----------------------------- PROBLEM ----------------------------- #####
# Create the Problem object
problem = Problem(model=model, name='test')

step_0 = problem.add_step(StaticStep())
step_0.add_gravity_load()

step_1 = problem.add_step(StaticStep())
step_1.add_point_load(x=1000, z=-1000, node=nodes[0])
# Define the field outputs required
# fout = step_0.add_output(FieldOutput(name='fout'))


# Review
# problem.summary()
# problem.show()

# Solve the problem
# problem.write_input_file()
problem.analyse(path=Path(TEMP).joinpath('refactor'))

# # # ##### --------------------- POSTPROCESS RESULTS -------------------------- #####
# # # results = Results.from_problem(problem, fields=['u'])
# # # pprint(results.nodal)
