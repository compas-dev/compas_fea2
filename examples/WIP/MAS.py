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
        nodes.append(list(round(float(y)*1000, 0) for y in x.split(",")))

with open("C:/temp/MAS/input/start_1.txt", "r") as f:
    start_1=[]
    for x in f:
        start_1.append(int(x))

with open("C:/temp/MAS/input/end_1.txt", "r") as f:
    end_1=[]
    for x in f:
        end_1.append(int(x))
connectivity_1 = list(zip(start_1, end_1))

with open("C:/temp/MAS/input/start_3.txt", "r") as f:
    start_3=[]
    for x in f:
        start_3.append(int(x))

with open("C:/temp/MAS/input/end_3.txt", "r") as f:
    end_3=[]
    for x in f:
        end_3.append(int(x))
connectivity_3 = list(zip(start_3, end_3))

with open("C:/temp/MAS/input/start_pt.txt", "r") as f:
    start_pt=[]
    for x in f:
        start_pt.append(int(x))

with open("C:/temp/MAS/input/end_pt.txt", "r") as f:
    end_pt=[]
    for x in f:
        end_pt.append(int(x))
connectivity_pt = list(zip(start_pt, end_pt))

with open("C:/temp/MAS/input/supports.txt", "r") as f:
    supports=[]
    for x in f:
        supports.append(int(x))

with open("C:/temp/MAS/input/horizontal.csv", "r") as f:
    h_forces={}
    for x in f:
        line = list(round(float(y)*1000,0) for y in x.split(","))
        k = tuple(line[:3])
        v = line[3:]
        if k in h_forces:
            h_forces[k] = [h_forces[k][i] + v[i] for i in range(3)]
        else:
            h_forces[k] = v

with open("C:/temp/MAS/input/uplift.csv", "r") as f:
    uplift={}
    for x in f:
        line = list(round(float(y)*1000,0) for y in x.split(","))
        k = tuple(line[:3])
        v = line[3:]
        if k in uplift:
            uplift[k] = [uplift[k][i] + v[i] for i in range(3)]
        else:
            uplift[k] = v


# # for n, k in zip(nodes, h_forces):
# #     print(tuple(n), k)

# for node in nodes:
#     n = tuple(node)
#     for k in h_forces:
#         if n > k-10 and n < k +10:
#             print(node)

#### ------------------------------ MODEL ------------------------------ #####

model = Model(name='structural_model')

model.add_part(Part(name='part-1'))

i=0
for node in nodes:
    model.add_node(Node(xyz=node), part='part-1')
    node =tuple(node)
    if node in h_forces:
        print(i)
        i += 1

model.add_material(ElasticIsotropic(name='mat_A', E=29000, v=0.17, p=2.5e-9))
model.add_section(TrussSection(name='Truss_1', material='mat_A', A=200))
model.add_section(TrussSection(name='Truss_3', material='mat_A', A=600))
# model.add_section(BoxSection(name='section_A', material='mat_A', a=20, b=80, t1=5, t2=5, t3=5, t4=5))

for c in connectivity_1:
    model.add_element(element=TrussElement(connectivity=c, section='Truss_1'), part='part-1')

for c in connectivity_3:
    model.add_element(element=TrussElement(connectivity=c, section='Truss_3'), part='part-1')

for c in connectivity_pt:
    model.add_element(element=TrussElement(connectivity=c, section='Truss_1'), part='part-1')


model.add_assembly_set(Set(name='fixed', selection=supports, stype='nset'), instance='part-1-1')

i=0
for p in h_forces:
    selection = model.get_node_from_coordinates(p[0:3], tol=5)

    model.add_assembly_set(Set(name='pload_'+str(i), selection=selection, stype='nset'), instance='part-1-1')
    i+=1

##### ----------------------------- PROBLEM ----------------------------- #####

problem = Problem(name='mas', model=model)
problem.add_bcs(bcs=[FixedDisplacement(name='bc_fix', bset='fixed')])

i=0
loads=[]
for p in h_forces:
    selection = model.get_node_from_coordinates(p[0:2], 10)
    problem.add_load(load=PointLoad(name='pload_'+str(i), lset='pload_'+str(i), z=p[5]))
    loads.append('pload_'+str(i))
    i+=1

problem.add_load(load=GravityLoad(name='gravity', g=9806., x=0, y=0, z=-1))
problem.add_field_output(fout=FieldOutput(name='fout', node_outputs=['RF', 'CF', 'U'], element_outputs=['S']))
problem.add_history_output(hout=HistoryOutput(name='hout'))
problem.add_step(step=GeneralStaticStep(name='gravity', loads=['gravity'], field_outputs=['fout'], history_outputs=['hout']))
problem.add_step(step=GeneralStaticStep(name='pload', loads=loads, field_outputs=['fout'], history_outputs=['hout']))
# problem.write_input_file(path='C:/temp/mas')
problem.analyse(path='C:/temp/mas')
