******************************************************************************
Model
******************************************************************************

At the heart of every COMPAS FEA2 analysis or simulation is a model.
A model consists of nodes, elements and parts,
and defines connections, constraints and boundary conditions.

>>> from compas_fea2.model import Model
>>> model = Model()
>>> 

Nodes
=====

Nodes are the basic building blocks of a model.
They define the locations in space that define all other entities.

>>> from compas_fea2.model import Node
>>> node = Node(xyz=(0.,0.,0.))
>>> 
Node(...)
>>> node.x
0.0
>>> node.y
0.0
>>> node.z
0.0
>>> node.xyz
[0.0, 0.0, 0.0]
>>> node.point
Point(x=0.0, y=0.0, z=0.0)

Besides coordinates, nodes have many other (optional) attributes.

>>> node.mass
(None, None, None)
>>> node.temperature
>>>
>>> node.dof
{'x': True, 'y': True, 'z': True, 'xx': True, 'yy': True, 'zz': True}
>>> node.loads
{}
>>> node.displacements
{}

Nodes also have a container for storing calculation results.

>>> node.results
{}


Elements
========

Elements are defined by the nodes they connect to and a section.

>>>

Parts
=====
