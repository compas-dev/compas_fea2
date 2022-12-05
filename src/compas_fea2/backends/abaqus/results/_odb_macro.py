# odbRead.py
# A script to read the Abaqus/CAE Visualization module tutorial
# output database and read displacement data from the node at
# the center of the hemispherical punch.

from odbAccess import *

odb = openOdb(path='C:/temp/ETL/fun_arch.cfr.odb')

# Create a variable that refers to the
# last frame of the first step.

lastFrame = odb.steps['Step-1'].frames[-1]

# Create a variable that refers to the displacement 'U'
# in the last frame of the first step.

displacement = lastFrame.fieldOutputs['U']

# Create a variable that refers to the node set 'PUNCH'
# located at the center of the hemispherical punch.
# The set is  associated with the part instance 'PART-1-1'.

center = odb.rootAssembly.instances['PART-1-1'].\
    nodeSets['PUNCH']

# Create a variable that refers to the displacement of the node
# set in the last frame of the first step.

centerDisplacement = displacement.getSubset(region=center)

# Finally, print some field output data from each node
# in the node set (a single node in this example).

for v in centerDisplacement.values:
    print 'Position = ', v.position, 'Type = ', v.type
    print 'Node label = ', v.nodeLabel
    print 'X displacement = ', v.data[0]
    print 'Y displacement = ', v.data[1]
    print 'Displacement magnitude =', v.magnitude

odb.close()
