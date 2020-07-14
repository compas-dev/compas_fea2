import compas
from compas.geometry import Box
from compas.datastructures import Mesh

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


# Define materials
mat1 = ElasticIsotropic(name='mat1',E=29000,v=0.17,p=2.5e-9)
mat2 = ElasticIsotropic(name='mat2',E=25000,v=0.17,p=2.4e-9)

# Define sections
section_A = SolidSection(name='section_A', material=mat1)
section_B = BoxSection(name='section_B', material=mat2, a=50, b=100, t1=5, t2=5, t3=5, t4=5)


box = Box.from_width_height_depth(1000, 500, 300)
mesh = Mesh.from_shape(box)

nodes = []
for v in mesh.vertices():
    nodes.append(Node(v+1,mesh.vertex_coordinates(v)))

key_index = mesh.key_index()
vertices = list(mesh.vertices())
edges = [(key_index[u], key_index[v]) for u, v in mesh.edges()]

# Generate elements between nodes
elements = []
c=1
for e in edges:
    elements.append(BeamElement(c, [nodes[e[0]], nodes[e[1]]], section_B))
    c+=1

# Assign nodes and elements to a part
parts = []
for e in elements:
    parts.append(Part(name='part-' + str(e.key), nodes=e.connectivity, elements=[e]))

# Define sets for boundary conditions and loads
nset_fixed = Set('fixed', [nodes[0]])
nset_roller = Set('roller', [nodes[1]])
nset_pload = Set('pload', [nodes[0]])
sets = [nset_fixed, nset_roller, nset_pload]

# Create an instance of the part
instances = []
for part in parts:
    instances.append(Instance(name='instance-'+ part.name, part=part, sets=[]))

instances[0]= Instance(name='instance-0', part=parts[0], sets=sets)
# Build the assembly
assembly = Assembly(name='box', instances=instances)

# Assign boundary conditions to the node stes
bc1 = RollerDisplacementXZ('bc_roller',nset_roller)
bc2 = FixedDisplacement('bc_fix', nset_fixed)

# Assign a point load to the node set
pload1 = PointLoad('pload1', nset_pload, y=-1000)

# Define the field outputs required
fout = FieldOutput('my_fout')

# Define the analysis step
step = GeneralStaticStep('gstep', loads=[pload1], field_output=[fout])

# Create the Structure object
my_structure = Structure('test_structure', parts, assembly, [], [bc1, bc2], [step])
my_structure.write_input_file(path='C:/temp/test_structure')
# # print(my_structure)

# # Analyse the structure
# my_structure.analyse(path='C:/temp/test_structure')
