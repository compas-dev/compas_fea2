from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# Author(s): Andrew Liew (github.com/andrewliew), Francesco Ranaudo (github.com/franaudo)


__all__ = [
    'Parts',
]

class Parts(object):

    def __init__(self):
        pass

    def write_part_start(self, name):
        self.write_line('*Part, name={}'.format(name))

    def write_part_end(self):
        self.write_line(',')
        self.write_line('*End Part')
        self.write_line('**')
