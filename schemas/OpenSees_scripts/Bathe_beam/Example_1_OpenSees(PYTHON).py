from openseespy.opensees import *

from math import asin, sqrt

wipe()

model('Basic', '-ndm', 2)

node(1, 0.0, 0.0)
node(2, 20.0, 0.0)

fix(1,1,1,1)

coordTransf = "Linear"
geomTransf(coordTransf, 1)

E = 200000.0
Area= 0.1*1.0
Iz=1.0/12.0

eleType = 'elasticBeamColumn'
eleTag = 1
eleNodes = [1, 2]
eleArgs = [Area, E, Iz, 1]
element(eleType, eleTag, *eleNodes, *eleArgs)



timeSeries('Linear', 1)
pattern('Plain', 1, 1)
load(2, 0.0, -0.1, 0.0)

constraints('Plain')
numberer('RCM')
system('BandGen')
test('EnergyIncr', 1e-06, 100)
integrator('LoadControl', 1.0)
algorithm('Linear')
analysis('Static')
analyze(1)

nodeDisp(2)
