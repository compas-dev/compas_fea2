import compas_fea2
from compas_fea2.model import Model
from compas_fea2.problem import Problem

compas_fea2.set_backend('abaqus')

model = Model('test', 'testing...', author='tom')
problem = Problem('test2', model, author='tomtom')

print(model)
print(problem)
