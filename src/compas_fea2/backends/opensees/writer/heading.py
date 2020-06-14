
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# Author(s): Andrew Liew (github.com/andrewliew)


__all__ = [
    'Heading',
]


class Heading(object):

    def __init__(self):

        pass


    def write_heading(self):

        self.write_section('Heading')
        self.blank_line()
        self.write_line('wipe\nmodel basic -ndm 3 -ndf {0}'.format(self.ndof))
        self.blank_line()
        self.blank_line()
