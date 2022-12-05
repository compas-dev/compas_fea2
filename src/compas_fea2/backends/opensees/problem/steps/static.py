from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.steps import StaticStep
from compas_fea2.problem.steps import StaticRiksStep


class OpenseesStaticStep(StaticStep):
    """Opensees implementation of the :class:`LinearStaticStep`.\n
    """
    __doc__ += StaticStep.__doc__

    def __init__(self, max_increments=100, initial_inc_size=1, min_inc_size=0.00001, time=1, nlgeom=False, modify=True, name=None, **kwargs):
        super(OpenseesStaticStep, self).__init__(max_increments, initial_inc_size,
                                                 min_inc_size, time, nlgeom, modify, name=name, **kwargs)

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """

        return """#
{}
# - Displacements
#   -------------
{}
#
# - Loads
#   -----
{}
#
# - Predefined Fields
#   -----------------
{}
#
# - Output Requests
#   ---------------
{}

constraints Transformation
numberer RCM
system BandGeneral
test NormDispIncr 1.0e-6 6
algorithm Newton
integrator LoadControl 1

analysis Static

# analyze 10
analyze 1
loadConst -time 0.0

# set Results [open results.out "w"]]
# foreach

""".format(self._generate_header_section(),
                    self._generate_displacements_section(),
                    self._generate_loads_section(),
                    self._generate_fields_section(),
                    self._generate_output_section(),
                    )

    def _generate_header_section(self):
        return """#
# {0}
#
#
timeSeries Constant {1} -factor 1.0
""".format(self.name, self.problem._steps_order.index(self))

    def _generate_displacements_section(self):
        return '\n'.join([pattern.load._generate_jobdata(pattern.distribution) for pattern in self.displacements]) or '#'

    def _generate_loads_section(self):
        if self.loads:
            return "pattern Plain {0} {0} -fact 1 {{\n{1}\n}}".format(self.problem._steps_order.index(self),
                                                                    '\n'.join([pattern.load._generate_jobdata(pattern.distribution) for pattern in self.loads]))
        else:
            return '#'

    def _generate_fields_section(self):
        return '#'

    def _generate_output_section(self):
        data_section=['#']
        if self._field_outputs:
            for foutput in self._field_outputs:
                data_section.append(foutput._generate_jobdata())
        if self._history_outputs:
            for houtput in self._history_outputs:
                data_section.append(houtput._generate_jobdata())
        return '\n'.join(data_section)




class OpenseesStaticRiksStep(StaticRiksStep):
    def __init__(self, max_increments=100, initial_inc_size=1, min_inc_size=0.00001, time=1, nlgeom=False, modify=True, name=None, **kwargs):
        super().__init__(max_increments, initial_inc_size, min_inc_size, time, nlgeom, modify, name, **kwargs)
        raise NotImplementedError
