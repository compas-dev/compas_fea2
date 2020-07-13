from compas_fea2.backends.abaqus.components import Node
from compas_fea2.backends.abaqus.components import Concrete
from compas_fea2.backends.abaqus.components import ElasticIsotropic
from compas_fea2.backends.abaqus.components import BoxSection
from compas_fea2.backends.abaqus.components import SolidSection
from compas_fea2.backends.abaqus.components import BeamElement
from compas_fea2.backends.abaqus.components import SolidElement
from compas_fea2.backends.abaqus.components import FixedDisplacement
from compas_fea2.backends.abaqus.components import RollerDisplacementXZ
from compas_fea2.backends.abaqus.components import Part
from compas_fea2.backends.abaqus.components import Set
from compas_fea2.backends.abaqus.components import Assembly
from compas_fea2.backends.abaqus.components import Instance
from compas_fea2.backends.abaqus.components import GeneralStaticStep
from compas_fea2.backends.abaqus.components import PointLoad
from compas_fea2.backends.abaqus.components import FieldOutput

from compas_fea2.backends.abaqus import Structure

# Initialise the assembly object
model = Assembly(name='structural_model')

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

# Create the Problem object
my_problem = Structure(name='test_structure')

# Add the model to the problem
my_problem.set_assembly(assembly=model)

# Assign boundary conditions to the node stes
bc1 = RollerDisplacementXZ(name='bc_roller', bset='roller')
bc2 = FixedDisplacement(name='bc_fix', bset='fixed')
my_problem.add_bcs(bcs=[bc1, bc2])

# Define the analysis step
# Assign a point load to the node set
pload1 = PointLoad(name='pload1', lset=model.sets['pload'], y=-1000)
# Define the field outputs required
fout = FieldOutput(name='my_fout')
step = GeneralStaticStep(name='gstep', loads=[pload1], field_output=[fout])
my_problem.add_step(step=step)

# Solve the problem
# my_structure.write_input_file(path='C:/temp/test_structure')
my_problem.analyse(path='C:/temp/test_structure')
