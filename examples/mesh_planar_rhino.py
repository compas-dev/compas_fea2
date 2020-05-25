import rhinoscriptsyntax as rs

from compas_fea2.cad import rhino

from compas_fea2.backends.abaqus import Concrete
from compas_fea2.backends.abaqus import ElementProperties as Properties
from compas_fea2.backends.abaqus import GeneralStep
from compas_fea2.backends.abaqus import PointLoads
from compas_fea2.backends.abaqus import PinnedDisplacement
from compas_fea2.backends.abaqus import PrestressLoad
from compas_fea2.backends.abaqus import RollerDisplacementX
from compas_fea2.backends.abaqus import ShellSection
from compas_fea2.backends.abaqus import Steel
from compas_fea2.backends.abaqus import TrussSection
from compas_fea2.backends.abaqus import Structure


# Author(s): Andrew Liew (github.com/andrewliew)


# Structure

mdl = Structure(name='mesh_planar', path='C:/Temp/')

# Elements

rhino.add_nodes_elements_from_layers(mdl, mesh_type='ShellElement', layers=['elset_mesh', 'elset_plates'])
rhino.add_nodes_elements_from_layers(mdl, line_type='TrussElement', layers=['elset_tie'])

# Sets

rhino.add_sets_from_layers(mdl, layers=['nset_pin', 'nset_roller'])

# Materials

mdl.add([
    Concrete(name='mat_concrete', fck=50),
    Steel(name='mat_steel', fy=460),
])

# Sections

mdl.add([
    ShellSection(name='sec_planar', t=0.050),
    TrussSection(name='sec_tie', A=0.0001),
])

# Properties

mdl.add([
    Properties(name='ep_planar', material='mat_concrete', section='sec_planar', elset='elset_mesh'),
    Properties(name='ep_plate', material='mat_steel', section='sec_planar', elset='elset_plates'),
    Properties(name='ep_tie', material='mat_steel', section='sec_tie', elset='elset_tie'),
])

# Displacements

mdl.add([
    PinnedDisplacement(name='disp_pin', nodes='nset_pin'),
    RollerDisplacementX(name='disp_roller', nodes='nset_roller'),
])

# Loads

loads = {}
for i in rs.ObjectsByLayer('loads'):
    loads[mdl.check_node_exists(rs.PointCoordinates(i))] = {'y': float(rs.ObjectName(i))}

mdl.add([
    PointLoads(name='load_points', components=loads),
    PrestressLoad(name='load_prestress', elements='elset_tie', sxx=50*10**6),
])

# Steps

mdl.add([
    GeneralStep(name='step_bc', displacements=['disp_pin', 'disp_roller']),
    GeneralStep(name='step_prestress', loads=['load_prestress']),
    GeneralStep(name='step_load', loads=['load_points']),
])
mdl.steps_order = ['step_bc', 'step_prestress', 'step_load']

# Summary

mdl.summary()

# Run

mdl.analyse_and_extract(fields=['u', 'cf', 's', 'rf'])

cbar1 = [-4*10**6, 0]
cbar2 = [0, 2*10**6]

rhino.plot_data(mdl, step='step_prestress', field='sminp', cbar=cbar1, radius=0.01)
rhino.plot_data(mdl, step='step_prestress', field='smaxp', cbar=cbar2, radius=0.01)
rhino.plot_data(mdl, step='step_load', field='sminp', cbar=cbar1, radius=0.01)
rhino.plot_data(mdl, step='step_load', field='smaxp', cbar=cbar2, radius=0.01)
rhino.plot_data(mdl, step='step_load', field='smises', cbar=cbar2, radius=0.01)
rhino.plot_data(mdl, step='step_load', field='um', radius=0.01)
rhino.plot_principal_stresses(mdl, step='step_load', ptype='max', scale=1)
rhino.plot_principal_stresses(mdl, step='step_load', ptype='min', scale=1, rotate=1)
rhino.plot_concentrated_forces(mdl, step='step_load')
rhino.plot_reaction_forces(mdl, step='step_load')
