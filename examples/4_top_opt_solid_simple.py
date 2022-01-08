from compas_fea2.backends.abaqus.model import Model
from compas_fea2.backends.abaqus.model import Part
from compas_fea2.backends.abaqus.model import Node
from compas_fea2.backends.abaqus.model import ElasticIsotropic
from compas_fea2.backends.abaqus.model import SolidSection
from compas_fea2.backends.abaqus.model import SolidElement
from compas_fea2.backends.abaqus.model import NodesGroup
from compas_fea2.backends.abaqus.model import PinnedBC

from compas_fea2.backends.abaqus.problem import Problem
from compas_fea2.backends.abaqus.problem import PointLoad
from compas_fea2.backends.abaqus.problem import FieldOutput, HistoryOutput
from compas_fea2.backends.abaqus.problem import GeneralStaticStep

# from compas_fea2.interfaces.viewer.viewer import OptiViewer
from pathlib import Path
from compas_fea2 import TEMP
##### ----------------------------- MODEL ----------------------------- #####

# NOTE: units are in mm ton s

# Initialise the assembly object
model = Model(name='m')

# Add a Part to the model
model.add_part(Part(name='s'))

# Define materials
mat = ElasticIsotropic(name='mat_A', E=29000, v=0.17, p=2.5e-9)

# Define sections
sec = SolidSection(name='Sec_A', material=mat)
model.add_section(sec)

n = 10
s = 100
# Add nodes to the part
for z in range(n):
    for y in range(n):
        for x in range(n):
            model.add_node(Node(xyz=[x*s, y*s, z*s]), part='s')

# Generate elements between nodes
elements = []
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
            elements.append((SolidElement(connectivity=[a, b, c, d, e, f, g, h], section='Sec_A')))
model.add_elements(elements=elements, part='s')

# Define sets for boundary conditions and loads
# bset_pinned = NodesGroup(name='bset_pinned', selection=[x for x in range(n**2)])
# lset_pload = NodesGroup(name='pload', selection=[944, 945, 964, 965])
model.add_pin_bc(name='bc_pinned', part='s', nodes=[x for x in range(n**2)])
model.summary()
# model.show()

##### ----------------------------- PROBLEM ----------------------------- #####
# Create the Problem object
problem = Problem(name='test_opt', model=model)

# Define the analysis step
problem.add_step(GeneralStaticStep(name='pstep', nlgeom=True))

# Assign a point load to the node set
problem.add_point_load(name='pload', step='pstep', part='solid', nodes=[n**3-x-1 for x in range(n**2)], z=-1)

# Define the field outputs required
fout = FieldOutput(name='fout')
hout = HistoryOutput(name='fout')
problem.add_outputs((fout, hout), 'pstep')
# Define the optimisation parameters
problem.set_optimisation_parameters(0.2, 50, 1)

# Get a summary
problem.summary()
# Solve the problem
# problem.analyse(path=Path(TEMP).joinpath(problem.name))
problem.optimise(path=Path(TEMP).joinpath(problem.name))

# # # Visualie results
# # v = OptiViewer(problem)
# # v.show()
