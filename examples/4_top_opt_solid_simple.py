from compas_fea2.backends.abaqus import Model
from compas_fea2.backends.abaqus import Part
from compas_fea2.backends.abaqus import Node
from compas_fea2.backends.abaqus import ElasticIsotropic
from compas_fea2.backends.abaqus import SolidSection
from compas_fea2.backends.abaqus import SolidElement
from compas_fea2.backends.abaqus import Set

from compas_fea2.backends.abaqus.problem import Problem
from compas_fea2.backends.abaqus import PinnedDisplacement
from compas_fea2.backends.abaqus import PointLoad
from compas_fea2.backends.abaqus import FieldOutput
from compas_fea2.backends.abaqus import GeneralStaticStep


##### ----------------------------- MODEL ----------------------------- #####

# NOTE: units are in mm ton s

# Initialise the assembly object
model = Model(name='structural_model')

# Add a Part to the model
model.add_part(Part(name='part-1'))

# Define materials
model.add_material(ElasticIsotropic(name='mat_A', E=29000, v=0.17, p=2.5e-9))

# Define sections
sec = SolidSection(name='section_A', material='mat_A')
model.add_section(sec)

n = 10
s = 100
# Add nodes to the part
for z in range(n):
    for y in range(n):
        for x in range(n):
            model.add_node(Node(xyz=[x*s, y*s, z*s]), part='part-1')

# Generate elements between nodes
elements=[]
for z in range(n-1):
    for y in range(n-1):
        for x in range(n-1):
            a = x+y*n+z*n**2
            b = (x+1)+y*n+z*n**2
            c = (x+1)+(y+1)*n+z*n**2
            d = x+(y+1)*n+z*n**2
            e = x+y*n+(z+1)*n**2
            f = (x+1)+y*n+(z+1)*n**2
            g = (x+1)+(y+1)*n+(z+1)*n**2
            h = x+(y+1)*n+(z+1)*n**2
            elements.append((SolidElement(connectivity=[a,b,c,d,e,f,g,h], section='section_A')))
model.add_elements(elements=elements, part='part-1')

# Define sets for boundary conditions and loads
model.add_assembly_set(Set(name='pinned', selection=[x for x in range(n**2)], stype='nset'), instance='part-1-1')
model.add_assembly_set(Set(name='pload', selection=[944,945,964,965], stype='nset'), instance='part-1-1')

model.summary()

##### ----------------------------- PROBLEM ----------------------------- #####
# Create the Problem object
problem = Problem(name='test_solid_structure', model=model)

# Assign boundary conditions to the node stes
problem.add_bcs(bcs=[PinnedDisplacement(name='bc_fix', bset='pinned')])

# Assign a point load to the node set
problem.add_load(load=PointLoad(name='pload', lset='pload', y=-1000))

# Define the field outputs required
problem.add_field_output(fout=FieldOutput(name='fout'))

# Define the analysis step
problem.add_step(step=GeneralStaticStep(name='gstep', loads=['pload']))

# Define the optimisation parameters
problem.set_optimisation_parameters(0.2, 40, 10)

# Get a summary
problem.summary()

# Solve the problem
problem.optimise()

