from compas_fea2.backends.abaqus import Model
from compas_fea2.backends.abaqus import Part
from compas_fea2.backends.abaqus import Node
from compas_fea2.backends.abaqus import ElasticIsotropic
from compas_fea2.backends.abaqus import SolidSection
from compas_fea2.backends.abaqus import SolidElement
from compas_fea2.backends.abaqus import Set

from compas_fea2.backends.abaqus.problem import Problem
from compas_fea2.backends.abaqus import FixedDisplacement
from compas_fea2.backends.abaqus import RollerDisplacementXZ
from compas_fea2.backends.abaqus import PointLoad
from compas_fea2.backends.abaqus import FieldOutput
from compas_fea2.backends.abaqus import GeneralStaticStep

import numpy as np



##### ----------------------------- MODEL ----------------------------- #####
# Initialise the assembly object
model = Model(name='structural_model')

# Add a Part to the model
model.add_part(Part(name='part-1'))

# Define materials
model.add_material(ElasticIsotropic(name='mat_A', E=29000, v=0.17, p=2.5e-9))

# Define sections
sec = SolidSection(name='section_A', material='mat_A')
model.add_section(sec)

size = 3
# Add nodes to the part
for z in range(size):
    for y in range(size):
        for x in range(size):
            model.add_node(Node(xyz=[x, y, z]), part='part-1')

# Generate elements between nodes
elements=[]
for z in range(size-1):
    for y in range(size-1):
        for x in range(size-1):
            a = x+y*size+z*size**2
            b = (x+1)+y*size+z*size**2
            c = (x+1)+(y+1)*size+z*size**2
            d = x+(y+1)*size+z*size**2
            e = x+y*size+(z+1)*size**2
            f = (x+1)+y*size+(z+1)*size**2
            g = (x+1)+(y+1)*size+(z+1)*size**2
            h = x+(y+1)*size+(z+1)*size**2
            elements.append((SolidElement(connectivity=[a,b,c,d,e,f,g,h], section='section_A')))
model.add_elements(elements=elements, part='part-1')

# Define sets for boundary conditions and loads
model.add_assembly_set(Set(name='fixed', selection=[0], stype='nset'), instance='part-1-1')
model.add_assembly_set(Set(name='roller', selection=[10], stype='nset'), instance='part-1-1')
model.add_assembly_set(Set(name='pload', selection=[20], stype='nset'), instance='part-1-1')

model.summary()

##### ----------------------------- PROBLEM ----------------------------- #####
# Create the Problem object
problem = Problem(name='test_solid_structure', model=model)

# Assign boundary conditions to the node stes
problem.add_bcs(bcs=[RollerDisplacementXZ(name='bc_roller', bset='roller'),
                        FixedDisplacement(name='bc_fix', bset='fixed')])

# Assign a point load to the node set
problem.add_load(load=PointLoad(name='pload', lset='pload', y=-1000))

# Define the field outputs required
problem.add_field_output(fout=FieldOutput(name='fout'))

# Define the analysis step
problem.add_step(step=GeneralStaticStep(name='gstep', loads=['pload']))

# Solve the problem
problem.summary()

problem.write_input_file()



# x_range = np.linspace(0,100,size,endpoint=False)
# y_range = np.linspace(0,100,size,endpoint=False)
# z_range = np.linspace(0,100,size,endpoint=False)

# xx,yy,zz = np.meshgrid(x_range, y_range, z_range)


# coord = [0,50,50]
# coord_idx = np.argwhere((xx==coord[1]) & (yy==coord[0]) & (zz==coord[2]))[0]
# num_inx = (coord_idx[0]+coord_idx[1]*size+coord_idx[2]*size**2)+1

