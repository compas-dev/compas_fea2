# import compas_fea2

from compas.datastructures import Mesh

# from compas_fea2.model import Model
from compas_fea2.model import ElasticIsotropic
from compas_fea2.model import ShellSection
from compas_fea2.model import Part
from compas_fea2.model import Node
from compas_fea2.model import ShellElement
# from compas_fea2.problem import Problem

# compas_fea2.set_backend('abaqus')

mesh = Mesh.from_meshgrid(10, 10)

part = Part()

material = ElasticIsotropic(E=210e+6, v=0.2, density=7850)
section = ShellSection(material=material, t=0.05)

part.add_material(material)
part.add_section(section)

vertex_node = {}
for vertex in mesh.vertices():
    point = mesh.vertex_coordinates(vertex)
    node = Node(point)
    part.add_node(node)
    vertex_node[vertex] = node

for face in mesh.faces():
    nodes = [vertex_node[vertex] for vertex in mesh.face_vertices(face)]
    element = ShellElement(nodes=nodes, section=section)
    part.add_element(element)

print(part)
