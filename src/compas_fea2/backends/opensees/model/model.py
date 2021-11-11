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
        self._backend = 'opensees'

    def _generate_jobdata(self):
        pass


# =============================================================================
#                               Debugging
# =============================================================================
if __name__ == "__main__":
    pass
