from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Author(s): Andrew Liew (github.com/andrewliew), Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'NodeBase',
]


class NodeBase(object):
    """Initialises base Node object.

    Parameters
    ----------
    xyz : list
        [x, y, z] co-ordinates of the node.
    ex : list
        Node's local x axis.
    ey : list
        Node's local y axis.
    ez : list
        Node's local z axis.
    mass : float
        Mass in kg associated with the node.
    label : string
        Node's label. If no label is specified, it is automatically generated
        when a node is added. The label does not need to be unique.

    key : int
        Node key number. The key number is unique.
    x : float
        x co-ordinates of the node.
    y : float
        y co-ordinates of the node.
    z : float
        z co-ordinates of the node.
    ex : list
        Node's local x axis.
    ey : list
        Node's local y axis.
    ez : list
        Node's local z axis.
    mass : float
        Mass in kg associated with the node.
    label : string
        Node's label. If no label is specified, it is automatically generated
        when a node is added. The label does not need to be unique.
    gkey : string
        Node's geometric key to uniquely identify it. The geometric key is built
        as: x_y_z

    Examples
    --------
    >>> node = Node(1.0, 2.0, 3.0)
    """

    def __init__(self, xyz, ex=None, ey=None, ez=None, mass=None, label=None):
        self.__name__ = 'Node'
        self.key      = 0
        self.xyz      = [float(x) for x in xyz]
        self.x        = self.xyz[0]
        self.y        = self.xyz[1]
        self.z        = self.xyz[2]
        self.ex       = ex
        self.ey       = ey
        self.ez       = ez
        self.mass     = mass
        self.label    = label
        self.gkey     = '{}_{}_{}'.format(self.x, self.y, self.z)

    def __str__(self):
        title = 'compas_fea2 {0} object'.format(self.__name__)
        separator = '-' * (len(self.__name__) + 19)
        l = []
        for attr in ['label', 'key', 'x', 'y', 'z', 'ex', 'ey', 'ez', 'mass']:
            l.append('{0:<10} : {1}'.format(attr, getattr(self, attr)))

        return """\n{}\n{}\n{}""".format(title, separator, '\n'.join(l))

    def __repr__(self):

        return '{0}({1} - {2})'.format(self.__name__, self.key, self.label)
