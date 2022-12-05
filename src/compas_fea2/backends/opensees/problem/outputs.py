from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.outputs import FieldOutput, HistoryOutput
from typing import Iterable

class OpenseesFieldOutput(FieldOutput):
    """"""
    __doc__ += FieldOutput.__doc__

    def __init__(self, node_outputs=None, element_outputs=None, nodes_set=None, elements_set=None, frequency=1, name=None, **kwargs):
        super(OpenseesFieldOutput, self).__init__(node_outputs=node_outputs,
                                                  element_outputs=element_outputs,
                                                  contact_outputs=None,
                                                  name=name, **kwargs)
        self.nodes_set = nodes_set
        self.elements_set = elements_set

    def _generate_jobdata(self):
        node_outputs = {
            'u':  '1 2 3 disp',
            'ur': '4 5 6 disp',
            'rf': '1 2 3 reaction',
            'rm': '4 5 6 reaction',
        }

        element_outputs = {
            "sf": '1 2 3 4 5 6 force',
            "s": '1 2 3 4 5 6 stresses'
        }
        data = ['#']
        if not self.node_outputs and not self.element_outputs:
            self.node_outputs = list(node_outputs.keys())
            self.element_outputs = list(element_outputs.keys())
        if self.node_outputs:
            for field in self.node_outputs:
                field = field.lower()
                if field in node_outputs:
                    output = node_outputs[field]
                    if not self.nodes_set:
                        key_range = f"0 {list(self.model.parts)[0].nodes_count}" #NOTE There is no support for parts atm
                        data.append(f'recorder Node -file {field}.out -time -nodeRange {key_range} -dof {output}')
                        data.append(f'recorder Node -xml {field}.xml -time -nodeRange {key_range} -dof {output}')

                    elif isinstance(self.nodes_set, range) and self.nodes_set.step == 1: #NOTE this is not really a range because the step is always 1
                        key_range = f"{self.nodes_set[0]} {self.nodes_set[-1]}"
                        data.append(f'recorder Node -file {self.name}_{field}.out -time -nodeRange {key_range} -dof {output}')
                    else:
                        if not isinstance(self.nodes_set, Iterable):
                            self.nodes_set = [self.nodes_set]
                        key_range = " ".join(str(key) for key in self.nodes_set)
                        data.append(f'recorder Node -file {self.name}_{field}.out -time -nodes {key_range} -dof {output}')

        if self.element_outputs:
            for field in self.element_outputs:
                field = field.lower()
                if field in element_outputs:
                    key_range = f"0 {list(self.model.parts)[0].elements_count}" #NOTE There is no support for parts atm
                    output = element_outputs[field]
                    data.append(f'recorder Element -file {field}.out -time -eleRange {key_range} -dof {output}')
                    data.append(f'recorder Element -xml {field}.xml -time -eleRange {key_range} -dof {output}')


        return '\n'.join(data)

#     """recorder Node -file Node3.out -time -node 3 -dof 1 2 disp
# recorder Element -file Element1.out -time -ele 1 force
# """

class OpenseesHistoryOutput(HistoryOutput):
    """"""
    __doc__ += HistoryOutput.__doc__

    def __init__(self):
        super(OpenseesHistoryOutput, self).__init__()
        raise NotImplementedError
