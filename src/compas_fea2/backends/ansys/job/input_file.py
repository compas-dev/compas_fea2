from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.job.input_file import InputFile
from compas_fea2.job.input_file import ParametersFile


class AnsysInputFile(InputFile):
    """ Ansys implementation of :class:`.InputFile`.\n
    """
    __doc__ += InputFile.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysInputFile, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysParametersFile(ParametersFile):
    """ Ansys implementation of :class:`.ParametersFile`.\n
    """
    __doc__ += ParametersFile.__doc__

    def __init__(self, name=None, **kwargs):
        super(AnsysParametersFile, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError
