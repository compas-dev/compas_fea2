from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.backends._core import NodeBase

# Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'Node',
]


# ==============================================================================
# General
# ==============================================================================

class Node(NodeBase):
    def __init__(self, key, xyz, ex=None, ey=None, ez=None, mass=None):
        super(Node, self).__init__(key, xyz, ex, ey, ez, mass)
        self.keyword = '*Node\n'
        self.data = self._generate_data()

    def _generate_data(self):
        x, y, z = self.xyz
        return ' {0},    {1:.3f},    {2:.3f},    {3:.3f}\n'.format(self.key, x, y, z)


if __name__ == "__main__":
    from compas_fea2.backends.abaqus.components import Node

    n = Node(1,[2,3,4])
    print(n.keyword)
