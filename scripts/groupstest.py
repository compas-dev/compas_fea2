from compas_fea2.model import Model, Part, Steel, SolidSection, Node
from compas_fea2.model import PartsGroup, ElementsGroup, NodesGroup


mdl = Model(name="multibay")
prt = mdl.add_part(name="part1")

nodes = [Node(xyz=[i, x, 0]) for i, x in enumerate(range(10))]
ng = NodesGroup(nodes=nodes, name="test")
print(ng)

ng_sg = ng.create_subgroup(name="x1", condition=lambda n: n.x == 1)
print(ng_sg)

new_group = ng-ng_sg
print(new_group)
# prt.add_nodes(nodes)
# print(mdl)
