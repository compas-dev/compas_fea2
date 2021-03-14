from compas_fea2.backends.abaqus import Model
from compas_fea2.backends.abaqus import Part
from compas_fea2.backends.abaqus import Node
from compas_fea2.backends.abaqus import ElasticIsotropic
from compas_fea2.backends.abaqus import BoxSection
from compas_fea2.backends.abaqus import ShellSection
from compas_fea2.backends.abaqus import BeamElement
from compas_fea2.backends.abaqus import Set

from compas_fea2.backends.abaqus import Problem
from compas_fea2.backends.abaqus import FixedDisplacement
from compas_fea2.backends.abaqus import RollerDisplacementXZ
from compas_fea2.backends.abaqus import PointLoad
from compas_fea2.backends.abaqus import FieldOutput
from compas_fea2.backends.abaqus import GeneralStaticStep

from compas_fea2 import DATA
from compas_fea2 import TEMP

import gmsh
import sys
from compas.datastructures import Mesh

def gmesh_to_compas(gmshModel):
    nodes = gmshModel.mesh.getNodes()
    node_tags = nodes[0]
    node_coords = nodes[1].reshape((-1, 3), order='C')
    node_paramcoords = nodes[2]
    xyz = {}
    for tag, coords  in zip(node_tags, node_coords):
        xyz[int(tag)] = coords.tolist()
    elements = gmshModel.mesh.getElements()
    triangles = []
    for etype, etags, ntags in zip(*elements):
        if etype == 2:
            for i, etag in enumerate(etags):
                n = gmshModel.mesh.getElementProperties(etype)[3]
                triangle = ntags[i * n: i * n + n]
                triangles.append(triangle.tolist())
    return Mesh.from_vertices_and_faces(xyz, triangles)

def gmsh_geometry(lc = 50):
    gmsh.initialize(sys.argv)
    gmsh.model.add("t1")

    gmsh.model.geo.addPoint(0, 0, 0, lc, 1)
    gmsh.model.geo.addPoint(1000, 0, 0, lc, 2)
    gmsh.model.geo.addPoint(1000, 3000, 0, lc, 3)
    p4 = gmsh.model.geo.addPoint(0, 3000, 0, lc)
    gmsh.model.geo.addLine(1, 2, 1)
    gmsh.model.geo.addLine(3, 2, 2)
    gmsh.model.geo.addLine(3, p4, 3)
    gmsh.model.geo.addLine(4, 1, p4)
    gmsh.model.geo.addCurveLoop([4, 1, -2, 3], 1)
    gmsh.model.geo.addPlaneSurface([1], 1)

    gmsh.model.geo.synchronize()
    gmsh.model.addPhysicalGroup(1, [1, 2, 4], 5)
    ps = gmsh.model.addPhysicalGroup(2, [1])
    gmsh.model.setPhysicalName(2, ps, "My surface")

    # We can then generate a 2D mesh...
    gmsh.model.mesh.generate(2)
    print(gmsh.model.mesh.getNode(nodeTag=10))
    element = gmsh.model.mesh.getElement(10)
    # gmsh.model.mesh.getElementFaceNodes()
    # print(gmsh.model.mesh.getKeysForElement(1,'Lagrange'))

    # ... and save it to disk
    gmsh.write(DATA+"/t1.stl")
    mesh = gmesh_to_compas(gmsh.model)
    gmsh.finalize()
    return mesh

mesh = gmsh_geometry()

##### ----------------------------- MODEL ----------------------------- #####
# Initialise the assembly object
model = Model(name='cantilever_gmsh')

# Define materials
model.add_material(ElasticIsotropic(name='mat_A', E=29000, v=0.17, p=2.5e-9))

# Define sections
shell_20 = ShellSection(name='section_A', material='mat_A', t=20)

# Create a shell model from a mesh
model.shell_from_mesh(mesh=mesh, shell_section=shell_20)

# Find nodes in the model for the boundary conditions
n_fixed = model.get_node_from_coordinates([0, 0, 0,], 1)
n_roller  = model.get_node_from_coordinates([1000, 0, 0], 1)
n_load = model.get_node_from_coordinates([1000, 3000, 0,], 1)

# Define sets for boundary conditions and loads
model.add_assembly_set(Set(name='fixed', selection=[n_fixed['part-1']], stype='nset'), instance='part-1-1')
model.add_assembly_set(Set(name='roller', selection=[n_roller['part-1']], stype='nset'), instance='part-1-1')
model.add_assembly_set(Set(name='pload', selection=[n_load['part-1']], stype='nset'), instance='part-1-1')

model.summary()

##### ----------------------------- PROBLEM ----------------------------- #####

# Create the Problem object
problem = Problem(name='cantilever_gmsh', model=model)

# Assign boundary conditions to the node stes
problem.add_bcs(bcs=[RollerDisplacementXZ(name='bc_roller', bset='roller'),
                        FixedDisplacement(name='bc_fix', bset='fixed')])

# Assign a point load to the node set
problem.add_load(load=PointLoad(name='pload', lset='pload', x=1000))

# Define the analysis step
problem.add_step(step=GeneralStaticStep(name='gstep', loads=['pload']))

problem.summary()

# Solve the problem
problem.analyse(path= TEMP + '/cantilever_gmsh')
problem.extract()

print(problem.results)
