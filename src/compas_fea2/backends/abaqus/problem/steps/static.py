from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.steps import StaticStep
from compas_fea2.problem.steps import StaticRiksStep


class AbaqusStaticStep(StaticStep):
    """"""
    __doc__ += StaticStep.__doc__
    """
    Note
    ----
    the data for the input file for this object is generated at runtime.

    """
    __doc__ += StaticStep.__doc__

    def __init__(self, max_increments=100, initial_inc_size=1, min_inc_size=0.00001, time=1, nlgeom=False, modify=True, name=None, **kwargs):
        super(AbaqusStaticStep, self).__init__(max_increments, initial_inc_size,
                                               min_inc_size, time, nlgeom, modify, name=name, **kwargs)
        self._stype = 'Static'

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """

        return f"""**
{self._generate_header_section()}**
** - Displacements
**   -------------
{self._generate_displacements_section()}**
** - Loads
**   -----
{self._generate_loads_section()}**
** - Output Requests
**   ---------------
{self._generate_output_section()}**
*End Step"""

    def _generate_header_section(self):
        data_section = []
        line = ("** STEP: {0}\n"
                "**\n"
                "*Step, name={0}, nlgeom={1}, inc={2}\n"
                "*{3}\n"
                "{4}, {5}, {6}, {5}\n").format(self._name, self._nlgeom, self._max_increments, self._stype, self._initial_inc_size, self._time, self._min_inc_size)
        data_section.append(line)
        return ''.join(data_section)

    def _generate_displacements_section(self):
        data_section = []
        for part in self.displacements:
            data_section += [displacement._generate_jobdata('{}-1'.format(part.name), node)
                             for node, displacement in self.displacements[part].items()]
        return '\n'.join(data_section)

    def _generate_loads_section(self):
        data_section = []
        if self.gravity:
            data_section.append(self._gravity._generate_jobdata())
        for part in self.loads:
            data_section += [load._generate_jobdata('{}-1'.format(part.name), nodes)
                             for load, nodes in self.loads[part].items()]
        return '\n'.join(data_section)

    def _generate_output_section(self):
        # TODO check restart option
        data_section = ["**",
                        "*Restart, write, frequency=0",
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
        raise NotImplementedError()
