from compas_fea2.backends.opensees.model import Model
from compas_fea2.backends.opensees.model import Part
from compas_fea2.backends.opensees.model import Node
from compas_fea2.backends.opensees.model import ElasticIsotropic
from compas_fea2.backends.opensees.model import RectangularSection
from compas_fea2.backends.opensees.model import BeamElement

nodes = [Node(node) for node in [[0., 0., 0.], [20., 0., 0., ]]]
mat = ElasticIsotropic('el_iso', 200000.0, 0.2, 10)
sec = RectangularSection('srec', 100, 1000, mat)


# set eleTag  1;
# set A       [expr 0.1*1];
# set E       200000.0;
# set Iz      [expr 0.1*1/12.0];
# element elasticBeamColumn $eleTag 1 2 $A $E $Iz $LinearTransf

# fix     1       1       1       1;
