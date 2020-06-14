"""
Author(s): Andrew Liew (github.com/andrewliew)
"""
from math import pi

from compas_fea2.cad import rhino

from compas_fea2.backends.abaqus import RectangularSection
from compas_fea2.backends.abaqus import ShellSection
from compas_fea2.backends.abaqus import ElasticIsotropic
from compas_fea2.backends.abaqus import ElementProperties
from compas_fea2.backends.abaqus import GeneralDisplacement
from compas_fea2.backends.abaqus import GeneralStep
from compas_fea2.backends.abaqus import FixedDisplacement
from compas_fea2.backends.abaqus import GravityLoad
from compas_fea2.backends.abaqus import Structure


# Structure

mdl = Structure(name='beam_shell_rhino', path='C:/Temp/')

# Elements

layers = ['beams', 'shell']
rhino.add_nodes_elements_from_layers(mdl, line_type='BeamElement', mesh_type='ShellElement', layers=layers)

# Sets

rhino.add_sets_from_layers(mdl, layers=['supports'])

# Materials

mdl.add(ElasticIsotropic(name='mat_1', E=20*10**9, v=0.3, p=1500))
mdl.add(ElasticIsotropic(name='mat_2', E=30*10**9, v=0.3, p=1500))

# Sections

mdl.add(RectangularSection(name='bsec', b=0.1, h=.2))
mdl.add(ElementProperties(name='ep_1', material='mat_1', section='bsec', elsets=['beams']))

mdl.add(ShellSection(name='ssec', t=.1))
mdl.add(ElementProperties(name='ep_2', material='mat_2', section='ssec', elsets=['shell']))

# Displacements

mdl.add([FixedDisplacement(name='supports', nodes='supports')])

# Loads

mdl.add(GravityLoad(name='load_gravity', elements=['beams', 'shell']))

# Steps

mdl.add([
    GeneralStep(name='step_bc', displacements=['supports']),
    GeneralStep(name='step_load', loads=['load_gravity']),
])
mdl.steps_order = ['step_bc', 'step_load']

# Summary

mdl.analyse_and_extract(fields=['s'])

# rhino.plot_data(mdl, step='step_load', field='um', radius=0.1, colorbar_size=0.3)
