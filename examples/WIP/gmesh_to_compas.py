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
    # gmshModel.finalize()
    return Mesh.from_vertices_and_faces(xyz, triangles)

def compas_to_gmsh(mesh, lc=100, write_path=None, inspect=False):
    gmsh.initialize(sys.argv)
    gmsh.model.add("mesh")

    for v in mesh.vertices():
        gmsh.model.geo.addPoint(*mesh.vertex_coordinates(v), lc, v)

    # Generate elements between nodes
    key_index = mesh.key_index()
    faces = [[key_index[key]
                for key in mesh.face_vertices(face)] for face in mesh.faces()]

    c=1
    for n, f in enumerate(faces):
        n=n+1
        for i in range(len(f)):
            p1 = f[i]
            p2 = f[(i + 1) % len(f)]
            gmsh.model.geo.addLine(p1, p2, c)
            c+=1
        gmsh.model.geo.addCurveLoop([c-4, c-3, c-2, c-1], n)
        # gmsh.model.geo.addPlaneSurface([n], n)
        gmsh.model.geo.addSurfaceFilling([n], n)
    gmsh.model.geo.synchronize()
    gmsh.model.mesh.refine()
    gmsh.model.mesh.generate(2)
    if inspect:
        gmsh.fltk.run()
    if write_path:
        gmsh.write("{}/t1.stl".format(write_path))
    return gmsh.model


# Get a Mesh geometry to create the model
mesh = Mesh.from_obj(DATA + '/hypar.obj')
gmesh = compas_to_gmsh(mesh, write_path=TEMP)

mesh = gmesh_to_compas(gmshModel=gmesh)

##### ----------------------------- MODEL ----------------------------- #####
# Initialise the assembly object
model = Model(name='hypar_gmsh')

# Define materials
model.add_material(ElasticIsotropic(name='mat_A', E=29000, v=0.17, p=2.5e-9))

# Define sections
shell_20 = ShellSection(name='section_A', material='mat_A', t=20)

# Create a shell model from a mesh
model.shell_from_mesh(mesh=mesh, shell_section=shell_20)

# Find nodes in the model for the boundary conditions
n_fixed = model.get_node_from_coordinates([5000, 0, 0,], 10)
n_roller  = model.get_node_from_coordinates([0, 0, -5000], 10)
n_load = model.get_node_from_coordinates([0, 3000, 0,], 10)

# Define sets for boundary conditions and loads
model.add_assembly_set(Set(name='fixed', selection=[n_fixed['part-1']], stype='nset'), instance='part-1-1')
model.add_assembly_set(Set(name='roller', selection=[n_roller['part-1']], stype='nset'), instance='part-1-1')
model.add_assembly_set(Set(name='pload', selection=[n_load['part-1']], stype='nset'), instance='part-1-1')

model.summary()

##### ----------------------------- PROBLEM ----------------------------- #####

# Create the Problem object
problem = Problem(name='hypar_gmsh', model=model)

# Assign boundary conditions to the node stes
problem.add_bcs(bcs=[RollerDisplacementXZ(name='bc_roller', bset='roller'),
                        FixedDisplacement(name='bc_fix', bset='fixed')])

# Assign a point load to the node set
problem.add_load(load=PointLoad(name='pload', lset='pload', x=1000))

# Define the analysis step
problem.add_step(step=GeneralStaticStep(name='gstep', loads=['pload']))

problem.summary()

# Solve the problem
problem.analyse(path= TEMP + '/hypar_gmsh')
problem.extract()

print(problem.results)
