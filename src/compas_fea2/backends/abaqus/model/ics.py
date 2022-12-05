from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import InitialTemperatureField
from compas_fea2.model import InitialStressField


class AbaqusInitialTemperatureField(InitialTemperatureField):
    """Abaqus implementation of :class:`InitialTemperatureField`\n"""
    __doc__ += InitialTemperatureField.__doc__

    def __init__(self, temperature, name=None, **kwargs):
        super(AbaqusInitialTemperatureField, self).__init__(temperature, name, **kwargs)

    def _generate_jobdata(self, instance, nodes):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).

        """

        data_section = ['** Name: {} Type: Temperature Field'.format(self.name),
                        '*Initial Conditions, type=TEMPERATURE']
        for node in nodes:
            data_section += ['{}.{}, {}'.format(instance, node.key+1, self._t)]
        return '\n'.join(data_section)


class AbaqusInitialStressField(InitialStressField):
    """Abaqus implementation of :class:`InitialStressField`\n"""
    __doc__ += InitialStressField.__doc__

    def __init__(self, stress, name=None, **kwargs):
        super(AbaqusInitialStressField, self).__init__(stress, name, **kwargs)

    def _generate_jobdata(self, elements_groups):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).

        """

        data_section = ['** Name: {} Type: Stress Field'.format(self.name),
                        '*Initial Conditions, type=STRESS']
        for elements_group in elements_groups:
            data_section += ['{}_i, {}'.format(elements_group.name, ', '.join(str(s) for s in self._s))]
        return '\n'.join(data_section)
