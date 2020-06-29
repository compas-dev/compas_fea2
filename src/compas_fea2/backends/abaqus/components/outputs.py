from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'FieldOutput',
    'HistoryOutput',
]

#todo: this is the pre-made field output -> change to costumised
class FieldOutput():
    def __init__(self, name):
        self.__name__  = 'FieldOutputRequst'
        self.name      = name
        # self.domain    = domain
        # self.frequency = frequency
        # self.variables = variables
        self.data      = """** FIELD OUTPUT: {}
**
*Output, field, variable=PRESELECT
**\n""".format(self.name)

class HistoryOutput():
    def __init__(self, name):
        self.__name__  = 'FieldOutputRequst'
        self.name      = name
        # self.domain    = domain
        # self.frequency = frequency
        # self.variables = variables
        self.data      = """** HISTORY OUTPUT: {}
**
*Output, history, variable=PRESELECT
**\n""".format(self.name)
