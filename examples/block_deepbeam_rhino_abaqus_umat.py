"""
Author(s): Francesco Ranaudo (github.com/franaudo), Andrew Liew (github.com/andrewliew)
"""
from compas_fea2.cad import rhino

from compas_fea2.backends.abaqus import Umat_hooke_iso
from compas_fea2.backends.abaqus import ElementProperties as Properties
from compas_fea2.backends.abaqus import GeneralStep
from compas_fea2.backends.abaqus import PinnedDisplacement
from compas_fea2.backends.abaqus import PointLoad
from compas_fea2.backends.abaqus import SolidSection
from compas_fea2.backends.abaqus import Structure

import rhinoscriptsyntax as rs


# Author(s): Andrew Liew (github.com/andrewliew)


# Structure

mdl = Structure(name='block_deepbeam_rhino_umat', path='C:/temp/')

# Extrude

nz = 20
rhino.mesh_extrude(mdl, guid=rs.ObjectsByLayer('base_mesh')[0], layers=nz, thickness=1./nz,
                   blocks_name='elset_blocks')

# Sets

rhino.add_sets_from_layers(mdl, layers=['nset_load', 'nset_supports'])

# Materials
umat_path = 'C:/Code/COMPAS/compas_fea2/src/compas_fea2/backends/abaqus/components/umat/umat-hooke-iso.f'
mdl.add(Umat_hooke_iso(name='umat', E=10**(10), v=0.3, p=1, path=umat_path))

# Sections

mdl.add(SolidSection(name='sec_solid'))

# Properties

mdl.add(Properties(name='ep_solid', material='umat', section='sec_solid', elset='elset_blocks'))

# Displacements

mdl.add(PinnedDisplacement(name='disp_pinned', nodes='nset_supports'))

# Loads

mdl.add(PointLoad(name='load_point', nodes='nset_load', z=-1))

# Steps

mdl.add([
    GeneralStep(name='step_bc', displacements=['disp_pinned']),
    GeneralStep(name='step_load', loads=['load_point']),
])
mdl.steps_order = ['step_bc', 'step_load']

# Structure

#mdl.summary()

#print(mdl.materials['umat'].sub_path)

# Run
mdl.analyse(user_sub='umat', overwrite=False)
#mdl.analyse_and_extract(fields=['u', 's'], components=['ux', 'uy', 'uz', 'smises'], user_sub=True)

#rhino.plot_data(mdl, step='step_load', field='smises', cbar=[0, 2])
#rhino.plot_voxels(mdl, step='step_load', field='smises', cbar=[0, 2], vdx=1./nz)

#mdl.save_to_cfea()
