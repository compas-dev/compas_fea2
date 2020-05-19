
from compas_fea2.cad import rhino
from compas_fea2.backends.abaqus.core import ElasticIsotropic
from compas_fea2.backends.abaqus.core import ElementProperties as Properties
from compas_fea2.backends.abaqus.core import GeneralStep
from compas_fea2.backends.abaqus.core import GravityLoad
from compas_fea2.backends.abaqus.core import PinnedDisplacement
from compas_fea2.backends.abaqus.core import ShellSection
from compas_fea2.backends.abaqus.core import Structure


# Author(s): Andrew Liew (github.com/andrewliew)


# Structure

mdl = Structure(name='mesh_principal', path='C:/Temp/')

# Elements

rhino.add_nodes_elements_from_layers(mdl, mesh_type='ShellElement', layers='elset_mesh')

# Sets

rhino.add_sets_from_layers(mdl, layers='nset_pins')

# Materials

mdl.add(ElasticIsotropic(name='mat_elastic', E=10**12, v=0.3, p=1000))

# Sections

mdl.add(ShellSection(name='sec_plate', t=1))

# Properties

mdl.add(Properties(name='ep_plate', material='mat_elastic', section='sec_plate', elset='elset_mesh'))

# Displacements

mdl.add(PinnedDisplacement(name='disp_pinned', nodes='nset_pins'))

# Loads

mdl.add(GravityLoad(name='load_gravity', elements='elset_mesh'))

# Steps

mdl.add([
    GeneralStep(name='step_bc', displacements=['disp_pinned']),
    GeneralStep(name='step_load', loads=['load_gravity']),
])
mdl.steps_order = ['step_bc', 'step_load']

# Summary

mdl.summary()

# Run

mdl.analyse_and_extract(fields=['u', 's'])

rhino.plot_principal_stresses(mdl, step='step_load', ptype='max', scale=3)
rhino.plot_principal_stresses(mdl, step='step_load', ptype='min', scale=3)
