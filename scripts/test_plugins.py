# import compas_fea2
from compas_fea2.model import Model
from compas_fea2.model import _Material
from compas_fea2.model import _Section, BoxSection
from compas_fea2.model import Part
from compas_fea2.problem import Problem

# compas_fea2.set_backend('abaqus')

model = Model(name='test', description='testing...', author='tom')
material = _Material(name='plastic', density=2400)
# steel = Steel(name='S355', fy=355, fu=None, eu=20, E=210, v=0.3, density=7850)
# concrete = Concrete(name='C20', fck=20, v=0.2, density=2400, fr=None)
section = _Section(name='section', material=material)
box = BoxSection(name='box', w=0.1, h=0.2, tw=0.005, tf=0.005, material=material)

problem = Problem('test2', model, author='tomtom')


print(model)
print(material)
# print(steel)
# print(concrete)
print(section)
print(box)

print(problem)


# for material in model.materials:
#     for part in model.parts:
#         for element in part.elements:
#             element.section.material = material

part = Part()

material = _Material()
section = _Section(material=material)

part.add_material(material)
part.add_section(section)

vertex_node = {}
for vertex in mesh.vertices():
    point = mesh.vertex_coordinates(vertex)
    node = part.add_node(Node(point))
    vertex_node[vertex] = node

for face in mesh.faces():
    nodes = [vertex_node[vertex] for vertex in mesh.face_vertices(face)]
    element = Element(nodes=nodes, section=section)
    part.add_element(element)
