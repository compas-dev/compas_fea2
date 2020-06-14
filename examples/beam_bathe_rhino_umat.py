
from compas.geometry import cross_vectors
from compas.geometry import normalize_vector
from compas.geometry import subtract_vectors

from compas_fea2.cad import rhino
from compas_fea2.backends.abaqus.core import FixedDisplacement
from compas_fea2.backends.abaqus.core import Umat_iso
from compas_fea2.backends.abaqus.core import ElementProperties as Properties
from compas_fea2.backends.abaqus.core import FixedDisplacement
from compas_fea2.backends.abaqus.core import GeneralStep
from compas_fea2.backends.abaqus.core import PointLoad
from compas_fea2.backends.abaqus.core import RectangularSection
from compas_fea2.backends.abaqus.core import Structure

import rhinoscriptsyntax as rs
import json


# Author(s): Andrew Liew (github.com/andrewliew)


# Local ex

for i in rs.ObjectsByLayer('elset_beams'):
    ez = subtract_vectors(rs.CurveEndPoint(i), rs.CurveStartPoint(i))
    ex = normalize_vector(cross_vectors(ez, [0, 0, 1]))
    rs.ObjectName(i, '_{0}'.format(json.dumps({'ex': ex})))

# Structure

mdl = Structure(name='beam_bathe_umat', path='C:/temp/')

# Elements

rhino.add_nodes_elements_from_layers(mdl, line_type='BeamElement', layers='elset_beams')

# Sets

rhino.add_sets_from_layers(mdl, layers=['nset_support', 'nset_load'])

# Materials

mdl.add(Umat_iso(name='umat_iso', E=10**7, v=0.2, p=1))

# Sections

mdl.add(RectangularSection(name='sec_beam', b=1, h=1))

# Properties

mdl.add(Properties(name='ep_beam', material='umat_iso', section='sec_beam', elset='elset_beams'))

# Displacements

mdl.add(FixedDisplacement(name='disp_fixed', nodes='nset_support'))

# Loads

mdl.add(PointLoad(name='load_point', nodes='nset_load', z=600))

# Steps

mdl.add([
    GeneralStep(name='step_bc', displacements=['disp_fixed']),
    GeneralStep(name='step_load', loads=['load_point']),
])
mdl.steps_order = ['step_bc', 'step_load']

# Summary

mdl.summary()


# Run

#mdl.analyse_and_extract(fields=['u', 'sf', 'sm'], license='research', cpus=2, umat='C:/Code/COMPAS/compas_fea2/src/compas_fea2/_core/umat/')
mdl.analyse_and_extract(fields=['u'], license='research', cpus=2, umat='C:/Code/COMPAS/compas_fea2/src/compas_fea2/_core/umat/')
#rhino.plot_data(mdl, step='step_load', field='uz', radius=1)
#
#print(mdl.get_nodal_results(step='step_load', field='uz', nodes='nset_load'))
