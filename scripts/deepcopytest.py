from compas_fea2.model import Model
from compas_fea2.model import DeformablePart
from compas_fea2.model import Node
from compas_fea2.model import BeamElement
from compas_fea2.model import RectangularSection
from compas_fea2.model import Steel


n1 = Node(xyz=[0, 0, 0])
n2 = Node(xyz=[1, 0, 0])
p1 = DeformablePart()
mdl1 = Model()

mat = Steel.S355()
sec = RectangularSection(w=1, h=2, material=mat)
beam = BeamElement(nodes=[n1, n2], section=sec, frame=[0, 0, 1])

# print(beam.__data__())

p1.add_element(beam)

mdl1.add_part(p1)
p1.add_node(n1)
p2 = p1.copy()
# print(mdl.__data__)

mdl2 = mdl1.copy()
mdl2.show()
# print(list(mdl1.parts)[0].nodes)
# print(list(mdl2.parts)[0].nodes)
# print(mdl2)
