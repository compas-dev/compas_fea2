from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Author(s): Francesco Ranaudo (github.com/franaudo)

from compas_fea2.backends._base.model import ModelBase

__all__ = [
    'Model',
]


class Model(ModelBase):
    """Initialises the Model object. This is in many aspects equivalent to an
    `Assembly` in Abaqus.
    """

    def __init__(self, name, description=None):
        super(Model, self).__init__(name, description)
        self._backend = 'abaqus'

    def _generate_data(self):
        section_data = ['*Assembly, name={}\n**\n'.format(self.name)]
        for instance in self.instances.values():
            section_data.append(instance._generate_data())
        # for surface in self.surfaces:
        #     section_data.append(surface.jobdata)
        # for constraint in self.constraints:
        #     section_data.append(constraint.jobdata)
        section_data.append('*End Assembly\n**\n')

        for iset in self.sets.values():
            section_data.append(iset._generate_data())
        return ''.join(section_data)


# =============================================================================
#                               Debugging
# =============================================================================
if __name__ == "__main__":
    pass
