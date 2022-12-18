from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.steps import StaticStep
from compas_fea2.problem.steps import StaticRiksStep


class AbaqusStaticStep(StaticStep):
    """"""
    __doc__ += StaticStep.__doc__
    """
    Warning
    -------
    In general steps the loads must be specified as total values, not incremental
    values. For example, if a concentrated load has a value of 1000 N in the
    first step and it is increased to 3000 N in the second general step, the
    magnitude given on the *CLOAD option in the two steps should be 1000 N and
    3000 N, not 1000 N and 2000 N.

    Note
    ----
    the data for the input file for this object is generated at runtime.

    """
    __doc__ += StaticStep.__doc__

    def __init__(self, max_increments=100, initial_inc_size=1, min_inc_size=0.00001, time=1, nlgeom=False, modify=True,
                 restart=False, name=None, **kwargs):
        super(AbaqusStaticStep, self).__init__(max_increments=max_increments,
                                               initial_inc_size=initial_inc_size,
                                               min_inc_size=min_inc_size,
                                               time=time,
                                               nlgeom=nlgeom,
                                               modify=modify,
                                               name=name, **kwargs)
        self._stype = 'Static'
        self._restart = restart

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """

        return """**
{}
** - Displacements
**   -------------
{}
**
** - Loads
**   -----
{}
**
** - Predefined Fields
**   -----------------
{}
**
** - Output Requests
**   ---------------
{}
**
*End Step""".format(self._generate_header_section(),
                    self._generate_displacements_section(),
                    self._generate_loads_section(),
                    self._generate_fields_section(),
                    self._generate_output_section(),
                    )

    def _generate_header_section(self):
        data_section = []
        line = ("** STEP: {0}\n"
                "**\n"
                "*Step, name={0}, nlgeom={1}, inc={2}\n"
                "*{3}\n"
                "{4}, {5}, {6}, {5}").format(self._name, 'YES' if self._nlgeom else 'NO', self._max_increments, self._stype, self._initial_inc_size, self._time, self._min_inc_size)
        data_section.append(line)
        return ''.join(data_section)

    def _generate_displacements_section(self):
        return '\n'.join([pattern.load._generate_jobdata(pattern.distribution) for pattern in self.displacements]) or '**'

    def _generate_loads_section(self):
        return '\n'.join([pattern.load._generate_jobdata(pattern.distribution) for pattern in self.loads]) or '**'

    def _generate_fields_section(self):
        return '\n'.join([pattern.load._generate_jobdata(pattern.distribution) for pattern in self.fields]) or '**'

    def _generate_output_section(self):
        # TODO check restart option
        data_section = ["**",
                        "*Restart, write, frequency={}".format(self.restart or 0),
                        "**"]
        if self._field_outputs:
            for foutput in self._field_outputs:
                data_section.append(foutput._generate_jobdata())
        if self._history_outputs:
            for houtput in self._history_outputs:
                data_section.append(houtput._generate_jobdata())
        return '\n'.join(data_section)

class AbaqusStaticRiksStep(StaticRiksStep):
    def __init__(self, max_increments=100, initial_inc_size=1, min_inc_size=0.00001, time=1, nlgeom=False, modify=True, name=None, **kwargs):
        super().__init__(max_increments, initial_inc_size, min_inc_size, time, nlgeom, modify, name, **kwargs)
        raise NotImplementedError
