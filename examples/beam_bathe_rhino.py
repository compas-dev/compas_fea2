"""
Author(s): Andrew Liew (github.com/andrewliew)
"""

import json
import rhinoscriptsyntax as rs

from compas.geometry import cross_vectors
from compas.geometry import normalize_vector
from compas.geometry import subtract_vectors

from compas_fea2.cad import rhino

from compas_fea2.backends.abaqus import Structure

from compas_fea2.backends.abaqus import FixedDisplacement
from compas_fea2.backends.abaqus import ElasticIsotropic
from compas_fea2.backends.abaqus import ElementProperties
from compas_fea2.backends.abaqus import FixedDisplacement
from compas_fea2.backends.abaqus import GeneralStep
from compas_fea2.backends.abaqus import PointLoad
from compas_fea2.backends.abaqus import RectangularSection



# Local ex

for i in rs.ObjectsByLayer('elset_beams'):
    ez = subtract_vectors(rs.CurveEndPoint(i), rs.CurveStartPoint(i))
    ex = normalize_vector(cross_vectors(ez, [0, 0, 1]))
    rs.ObjectName(i, '_{0}'.format(json.dumps({'ex': ex})))

# Structure

mdl = Structure(name='beam_bathe2', path='C:/Temp/')

# Elements

rhino.add_nodes_elements_from_layers(mdl, line_type='BeamElement', layers='elset_beams')

# Sets

rhino.add_sets_from_layers(mdl, layers=['nset_support', 'nset_load'])

# Materials

mdl.add_material(ElasticIsotropic(name='mat_elastic', E=10**7, v=10**(-5), p=1))

# Sections

mdl.add_section(RectangularSection(name='sec_beam', b=1, h=1))

# Properties

mdl.add_element_properties(ElementProperties(name='ep_beam', material='mat_elastic', section='sec_beam', elset='elset_beams'))

# Displacements

mdl.add_displacement(FixedDisplacement(name='disp_fixed', nodes='nset_support'))

# Loads

mdl.add_load(PointLoad(name='load_point', nodes='nset_load', z=600))

# Steps

mdl.add_steps([
    GeneralStep(name='step_bc', displacements=['disp_fixed']),
    GeneralStep(name='step_load', loads=['load_point']),
])
mdl.steps_order = ['step_bc', 'step_load']

# Summary

mdl.summary()

# Run

mdl.analyse_and_extract(fields=['u', 'sf', 'sm'], save=True)
#
#rhino.plot_data(mdl, step='step_load', field='uz', radius=1)
