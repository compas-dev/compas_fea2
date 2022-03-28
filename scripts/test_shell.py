# import compas_fea2

from compas.datastructures import Mesh

# from compas_fea2.model import Model
from compas_fea2.model import ElasticIsotropic
from compas_fea2.model import ShellSection
from compas_fea2.model import Part
from compas_fea2.model import Node
from compas_fea2.model import ShellElement
# from compas_fea2.problem import Problem
import compas_fea2
compas_fea2.set_backend('abaqus')
compas_fea2.config.VERBOSE = True

mesh = Mesh.from_meshgrid(10, 10)

material = ElasticIsotropic(E=210e+6, v=0.2, density=7850)
section = ShellSection(material=material, t=0.05)

# part_shell = Part.shell_from_compas_mesh(mesh, section)
part_frame = Part.frame_from_compas_mesh(mesh, section)


# print(part_shell)
print(part_frame)
