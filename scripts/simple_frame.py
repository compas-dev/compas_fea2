
from compas_fea2.backends.abaqus.model import Model
from compas_fea2.backends.abaqus.model import Part
from compas_fea2.backends.abaqus.model import Node
from compas_fea2.backends.abaqus.model import ElasticIsotropic
from compas_fea2.backends.abaqus.model import BoxSection
from compas_fea2.backends.abaqus.model import BeamElement
from compas_fea2.backends.abaqus.model import Set

from compas_fea2.backends.abaqus.problem import Problem
from compas_fea2.backends.abaqus.problem import FixedDisplacement
from compas_fea2.backends.abaqus.problem import RollerDisplacementXZ
from compas_fea2.backends.abaqus.problem import PointLoad
from compas_fea2.backends.abaqus.problem import FieldOutput
from compas_fea2.backends.abaqus.problem import GeneralStaticStep

##### ----------------------------- MODEL ----------------------------- #####
# Initialise the assembly object
model = Model(name='structural_model')

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
model.add_section(BoxSection(name='section_A', material='mat_A', a=20, b=80, t1=5, t2=5, t3=5, t4=5))
model.add_section(BoxSection(name='section_B', material='mat_B', a=20, b=80, t1=5, t2=5, t3=5, t4=5))

# Generate elements between nodes
elements = []
for e in range(len(model.parts['part-1'].nodes)-1):
    elements.append((BeamElement(connectivity=[e, e+1], section='section_A')))
model.add_elements(elements=elements, part='part-1')
model.add_element(element=BeamElement(connectivity=[29, 0], section='section_B'), part='part-1')

# Define sets for boundary conditions and loads
model.add_assembly_set(Set(name='fixed', selection=[0], stype='nset'), instance='part-1-1')
model.add_assembly_set(Set(name='roller', selection=[10], stype='nset'), instance='part-1-1')
model.add_assembly_set(Set(name='pload', selection=[20], stype='nset'), instance='part-1-1')


##### ----------------------------- PROBLEM ----------------------------- #####
# Create the Problem object
problem = Problem(name='test_structure', assembly=model)

# Assign boundary conditions to the node stes
problem.add_bcs(bcs=[RollerDisplacementXZ(name='bc_roller', bset='roller'),
                        FixedDisplacement(name='bc_fix', bset='fixed')])

# Assign a point load to the node set
problem.add_load(load=PointLoad(name='pload', lset='pload', y=-1000))

# Define the field outputs required
problem.add_field_output(fout=FieldOutput(name='fout'))

# Define the analysis step
problem.add_step(step=GeneralStaticStep(name='gstep', loads=['pload'], field_output=['fout']))

# Solve the problem
# my_structure.write_input_file(path='C:/temp/test_structure')
problem.analyse(path='C:/temp/test_structure')
