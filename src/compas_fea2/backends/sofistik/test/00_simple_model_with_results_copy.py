import os
from pathlib import Path
import random

import compas
from compas.datastructures import Mesh

import compas_fea2
from compas_fea2.model import Model, DeformablePart, Node
from compas_fea2.model import RectangularSection, ElasticIsotropic, ShellSection
from compas_fea2.problem import Problem, StaticStep, FieldOutput

from compas_fea2.units import units
units = units(system='SI_mm')

from compas_fea2.model import GeneralBC

# compas_fea2.set_backend('abaqus')
#compas_fea2.set_backend('opensees')
compas_fea2.set_backend('sofistik')

HERE = os.path.dirname(__file__)
TEMP = os.sep.join(HERE.split(os.sep)[:-1]+['temp'])

mdl = Model(name='my_model')

lx = (7*units.m).to_base_units().magnitude
ly = (10*units.m).to_base_units().magnitude
nx = 10
ny = 10
mesh = Mesh.from_meshgrid(lx, nx, ly, ny)

mat = ElasticIsotropic(E=(210*units.GPa).to_base_units().magnitude, 
                       v=0.2, 
                       density=(7800*units("kg/m**3")).to_base_units().magnitude)
#sec = CircularSection(r=100, material=mat)
sec = RectangularSection(w=100, h=200, material=mat)
prt = DeformablePart.frame_from_compas_mesh(mesh, sec)

mdl.add_part(prt)

#fra
#fixed_nodes = [prt.find_node_by_key(vertex) for vertex in list(filter(lambda v: mesh.vertex_degree(v)==2, mesh.vertices()))]
#mdl.add_fix_bc(nodes=fixed_nodes)


# to get indices of fixed_nodes
# indxs = [indx for indx in mesh.vertices() if mesh.vertex_degree(indx) == 2]
# print(indxs)

#io
#bc_general = GeneralBC()
#mdl.add_bcs(bc=bc_general, nodes=fixed_nodes)


# DEFINE THE PROBLEM
# define a step
step_1 = StaticStep()
pt = prt.find_node_by_key(random.choice(list(filter(lambda v: mesh.vertex_degree(v)!=2, mesh.vertices()))))
step_1.add_point_load(nodes=[pt],
                        z=-(10*units.kN).to_base_units().magnitude)
#fout = FieldOutput(node_outputs=['U', 'RF']) #??
#step_1.add_output(fout) #??
#hout = HistoryOutput('hout_test')

# set-up the problem
prb = Problem('00_simple_problem', mdl)
prb.add_step(step_1)
# prb.summary()
# mdl.show(draw_bcs=1000)

mdl.add_problem(problem=prb)
prb.path = r"C:\Code\FROM_COMPAS\compas_fea2\temp"
prb.write_input_file() 
#mdl.show()

# #--------------- things from original FraRan file not needed at the moment ----------------#
# print(Path(TEMP).joinpath(prb.name))
# mdl.analyse(problems=[prb], path=Path(TEMP).joinpath(prb.name), verbose=True)

# prb.convert_results_to_sqlite(Path(TEMP).joinpath(prb.name, prb.name))

# # prb.show_deformed(scale_factor=100)
# prb.show_displacements()