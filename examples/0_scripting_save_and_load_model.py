from compas.datastructures import Mesh

from compas_fea2.backends.abaqus.model import Model
from compas_fea2.backends.abaqus.model import ElasticIsotropic
from compas_fea2.backends.abaqus.model import BoxSection


from compas_fea2 import DATA
from compas_fea2 import TEMP

# Get a Mesh geometry to create the model
mesh = Mesh.from_obj(DATA + '/hypar.obj')

##### ------------------------------ MODEL ------------------------------ #####
# Initialise the assembly object
model = Model(name='hypar')

# Define some properties
model.add_material(ElasticIsotropic(name='mat_A', E=29000, v=0.17, p=2.5e-9))
box_20_80 = BoxSection(name='section_A', material='mat_A', a=20, b=80, t1=5, t2=5, t3=5, t4=5)

# Create a frame model from a mesh
model.frame_from_mesh(mesh=mesh, beam_section=box_20_80)

# view model summary and save to cfm
model.summary()
print(model.parts['part-1'])
model.save_to_cfm(path= TEMP + '/hypar_frame')

# Initializa a new model from the cfm file
new_model = Model.load_from_cfm(filename= TEMP + '/hypar_frame/hypar.cfm')
new_model.summary()
print(new_model.parts['part-1'])
