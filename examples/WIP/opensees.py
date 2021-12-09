from pprint import pprint

from compas_fea2.backends.opensees.model import Model
from compas_fea2.backends.opensees.model import Part
from compas_fea2.backends.opensees.model import Node
from compas_fea2.backends.opensees.model import ElasticIsotropic
from compas_fea2.backends.opensees.model import RectangularSection
from compas_fea2.backends.opensees.model import BeamElement
# from compas_fea2.backends.opensees.model import Set

from compas_fea2.backends.opensees.problem import Problem
from compas_fea2.backends.opensees.problem import FixedDisplacement
from compas_fea2.backends.opensees.problem import PointLoad
# from compas_fea2.backends.opensees.problem import FieldOutput
from compas_fea2.backends.opensees.problem.steps import StaticLinearPertubationStep

# from compas_fea2.backends.opensees.results import Results

from compas.geometry import Polyline

from compas_view2 import app


##### ----------------------------- MODEL ----------------------------- #####
# Initialise the assembly object
model = Model(name='structural_model', description='test model for opensees')

# Add a Part to the model
model.add_part(Part(name='part-1'))

# Add nodes to the part
for x in range(0, 1100, 100):
    model.add_node(Node(xyz=[x, 0.0, 0.0]), part='part-1')
for y in range(100, 600, 100):
    model.add_node(Node(xyz=[x, y, 0.0]), part='part-1')
for x in range(900, -100, -100):
    model.add_node(Node(xyz=[x, y, 0.0]), part='part-1')
for y in range(400, 0, -100):
    model.add_node(Node(xyz=[x, y, 0.0]), part='part-1')

# Define materials
model.add_material(ElasticIsotropic(name='mat_A', E=29000, v=0.17, p=2.5e-9))
model.add_material(ElasticIsotropic(name='mat_B', E=25000, v=0.17, p=2.5e-9))

# Define sections
model.add_section(RectangularSection(name='section_A', b=100, h=300, material='mat_A'))

# Generate elements between nodes
elements = []
for e in range(len(model.parts['part-1'].nodes)-1):
    elements.append((BeamElement(connectivity=[e, e+1], section='section_A')))
model.add_elements(elements=elements, part='part-1')
model.add_element(element=BeamElement(connectivity=[29, 0], section='section_A'), part='part-1')

viewer = app.App()
pts = [pt.xyz for pt in model.parts['part-1'].nodes]

polyline = Polyline(pts)
viewer.add(polyline, show_points=True, pointcolor=(0, 0, 1), linecolor=(1, 0, 0), linewidth=5)

viewer.show()


# Define sets for boundary conditions and loads
# model.add_assembly_set(Set(name='fixed', selection=[0, 10, 20], stype='nset'), instance='part-1-1')


# ##### ----------------------------- PROBLEM ----------------------------- #####
# # Create the Problem object
# problem = Problem(name='test_structure', model=model)

# # Assign boundary conditions to the node stes
# problem.add_bcs(bcs=[FixedDisplacement(name='bc_fix', bset='fixed')])

# # Assign a point load to the node set
# problem.add_load(load=PointLoad(name='pload', lset='pload', y=-1000))

# # Define the field outputs required
# # problem.add_field_output(fout=FieldOutput(name='fout'))

# # Define the analysis step
# problem.add_step(step=StaticLinearPertubationStep(name='gstep', loads=['pload']))

# # Solve the problem
# problem.summary()
# problem.analyse()

# ##### --------------------- POSTPROCESS RESULTS -------------------------- #####
# results = Results.from_problem(problem, fields=['u'])
# print(results.nodal)
