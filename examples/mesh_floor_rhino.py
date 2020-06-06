from math import pi

import rhinoscriptsyntax as rs

from compas.datastructures import Mesh
from compas_rhino.geometry import RhinoMesh

from compas_fea2.cad import rhino

from compas_fea2.backends.abaqus import Concrete
from compas_fea2.backends.abaqus import ElementProperties as Properties
from compas_fea2.backends.abaqus import GeneralDisplacement
from compas_fea2.backends.abaqus import GeneralStep
from compas_fea2.backends.abaqus import GravityLoad
from compas_fea2.backends.abaqus import PinnedDisplacement
from compas_fea2.backends.abaqus import PrestressLoad
from compas_fea2.backends.abaqus import RectangularSection
from compas_fea2.backends.abaqus import RollerDisplacementXY
from compas_fea2.backends.abaqus import ShellSection
from compas_fea2.backends.abaqus import Steel
from compas_fea2.backends.abaqus import Stiff
from compas_fea2.backends.abaqus import Structure
from compas_fea2.backends.abaqus import TributaryLoad
from compas_fea2.backends.abaqus import TrussSection


# Author(s): Andrew Liew (github.com/andrewliew)


# Structure

mdl = Structure(name='mesh_floor', path='C:/Temp/')

# Elements

rhino.add_nodes_elements_from_layers(mdl, mesh_type='ShellElement', layers=['elset_ribs', 'elset_vault'])
rhino.add_nodes_elements_from_layers(mdl, line_type='BeamElement', layers='elset_stiff')
rhino.add_nodes_elements_from_layers(mdl, line_type='TrussElement', layers='elset_ties')

# Sets

rhino.add_sets_from_layers(mdl, layers=['nset_corner1', 'nset_corner2'])
edges = [i for i in mdl.nodes if mdl.nodes[i].z < 0.001]
mdl.add_set(name='nset_edges', type='node', selection=edges)

# Materials

mdl.add([
    Concrete(name='mat_concrete', fck=90, fr=[1.16, 0.15]),
    Stiff(name='mat_stiff', E=10**12),
    Steel(name='mat_steel', fy=355),
])

# Sections

mdl.add([
    ShellSection(name='sec_ribs', t=0.020),
    ShellSection(name='sec_vault', t=0.050),
    RectangularSection(name='sec_stiff', b=1, h=1),
    TrussSection(name='sec_ties', A=pi*0.25*0.030**2),
])

# Properties

mdl.add([
    Properties(name='ep_ribs', material='mat_concrete', section='sec_ribs', elset='elset_ribs'),
    Properties(name='ep_vault', material='mat_concrete', section='sec_vault', elset='elset_vault'),
    Properties(name='ep_stiff', material='mat_stiff', section='sec_stiff', elset='elset_stiff'),
    Properties(name='ep_ties', material='mat_steel', section='sec_ties', elset='elset_ties'),
])

# Displacements

mdl.add([
    RollerDisplacementXY(name='disp_edges', nodes='nset_edges'),
    PinnedDisplacement(name='disp_pinned', nodes='nset_corner1'),
    GeneralDisplacement(name='disp_xdof', nodes='nset_corner2', x=0),
])

# Loads

guid = rs.ObjectsByLayer('load_mesh')[0]
mesh = RhinoMesh.from_guid(guid).to_compas(cls=Mesh)

mdl.add([
    GravityLoad(name='load_gravity', elements=['elset_ribs', 'elset_vault']),
    PrestressLoad(name='load_prestress', elements='elset_ties', sxx=10*10**6),
    TributaryLoad(mdl, name='load_area', mesh=mesh, z=-2000),
])

# Steps

mdl.add([
    GeneralStep(name='step_bc', displacements=['disp_edges', 'disp_pinned', 'disp_xdof']),
    GeneralStep(name='step_loads', loads=['load_gravity', 'load_area'], factor={'load_gravity': 1.35, 'load_area': 1.50}),
])
mdl.steps_order = ['step_bc', 'step_loads']

# Summary

mdl.summary()

# Run

mdl.analyse_and_extract(fields=['u', 's', 'cf'], components=['ux', 'uy', 'uz', 'smises', 'cfx', 'cfy', 'cfz'])

rhino.plot_data(mdl, step='step_loads', field='uz', radius=0.02, cbar_size=0.5)
rhino.plot_data(mdl, step='step_loads', field='smises', radius=0.02, cbar_size=0.5, cbar=[0, 5*10**6])
rhino.plot_concentrated_forces(mdl, step='step_loads')

mdl.save_to_obj()
