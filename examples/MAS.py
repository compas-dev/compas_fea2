from compas_fea2.backends.abaqus import Model
from compas_fea2.backends.abaqus import Part
from compas_fea2.backends.abaqus import Node
from compas_fea2.backends.abaqus import ElasticIsotropic
from compas_fea2.backends.abaqus import BoxSection
from compas_fea2.backends.abaqus import TrussSection
from compas_fea2.backends.abaqus import BeamElement
from compas_fea2.backends.abaqus import TrussElement
from compas_fea2.backends.abaqus import Set

from compas_fea2.backends.abaqus import Problem
from compas_fea2.backends.abaqus import FixedDisplacement
from compas_fea2.backends.abaqus import RollerDisplacementXZ
from compas_fea2.backends.abaqus import PointLoad
from compas_fea2.backends.abaqus import GravityLoad
from compas_fea2.backends.abaqus import FieldOutput
from compas_fea2.backends.abaqus import HistoryOutput
from compas_fea2.backends.abaqus import GeneralStaticStep

##### ---------------------------- IMPORTS ------------------------------ #####

with open("C:/temp/MAS/input/points.txt", "r") as f:
    nodes=[]
    for x in f:
        nodes.append(list((float(y)*1000 for y in x.split(","))))

with open("C:/temp/MAS/input/start.txt", "r") as f:
    start=[]
    for x in f:
        start.append(int(x))

with open("C:/temp/MAS/input/end.txt", "r") as f:
    end=[]
    for x in f:
        end.append(int(x))
connectivity = list(zip(start, end))

with open("C:/temp/MAS/input/supports.txt", "r") as f:
    supports=[]
    for x in f:
        supports.append(int(x))

with open("C:/temp/MAS/input/loads.txt", "r") as f:
    loads=[]
    for x in f:
        loads.append(int(x))


##### ------------------------------ MODEL ------------------------------ #####

model = Model(name='structural_model')

model.add_part(Part(name='part-1'))

for node in nodes:
    model.add_node(Node(xyz=node), part='part-1')

model.add_material(ElasticIsotropic(name='mat_A', E=29000, v=0.17, p=2.5e-9))
model.add_section(TrussSection(name='Truss_A', material='mat_A', A=200))
# model.add_section(BoxSection(name='section_A', material='mat_A', a=20, b=80, t1=5, t2=5, t3=5, t4=5))

elements = []
for c in connectivity:
    model.add_element(element=TrussElement(connectivity=c, section='Truss_A'), part='part-1')
    # model.add_element(element=BeamElement(connectivity=c, section='section_A'), part='part-1')

model.add_assembly_set(Set(name='fixed', selection=supports, stype='nset'), instance='part-1-1')
model.add_assembly_set(Set(name='pload', selection=loads, stype='nset'), instance='part-1-1')


##### ----------------------------- PROBLEM ----------------------------- #####

problem = Problem(name='mas', model=model)
problem.add_bcs(bcs=[FixedDisplacement(name='bc_fix', bset='fixed')])
problem.add_load(load=PointLoad(name='pload', lset='pload', z=-10))
problem.add_load(load=GravityLoad(name='gravity', g=9806., x=0, y=0, z=-1))
problem.add_field_output(fout=FieldOutput(name='fout', node_outputs=['RF', 'CF', 'U'], element_outputs=['S']))
problem.add_history_output(hout=HistoryOutput(name='hout'))
problem.add_step(step=GeneralStaticStep(name='gravity', loads=['gravity'], field_outputs=['fout'], history_outputs=['hout']))
problem.add_step(step=GeneralStaticStep(name='pload', loads=['pload'], field_outputs=['fout'], history_outputs=['hout']))
# problem.write_input_file(path='C:/temp/mas')
problem.analyse(path='C:/temp/mas')
