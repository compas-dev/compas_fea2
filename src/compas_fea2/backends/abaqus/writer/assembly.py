from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# Author(s): Andrew Liew (github.com/andrewliew), Francesco Ranaudo (github.com/franaudo)


__all__ = [
    'Assembly',
    'Instances',
]

class Assembly(object):

    def __init__(self):
        pass

    def write_assembly_start(self, name):
        self.write_section('ASSEMBLY')
        self.write_line('*Assembly, name={}'.format(name))
        self.write_line('**')

    def write_assembly_end(self):
        self.write_line(',')
        self.write_line('*End Assembly')
        self.write_line('**')


class Instances(object):

    def __init__(self):
        pass

    def write_instance(self, instance_name, part_name):
        self.write_line('*Instance, name={}, part={}'.format(instance_name, part_name))
        self.write_line('*End Instance')
        self.write_line('**')
