from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.job.input_file import InputFile
from compas_fea2.job.input_file import ParametersFile

class SofistikInputFile(InputFile):
    """Sofistik implementation of :class:`compas_fea2.job.input_file.InputFile`.\n
    """
    __doc__ += InputFile.__doc__

    def __init__(self, name=None, **kwargs):
        super(SofistikInputFile, self).__init__(name=name, **kwargs)
        self._extension = 'dat'

    def _generate_jobdata(self):
        """Generate the content of the input file from the Model and Problem object.

        Parameters
        ----------
        problem : obj
            Problem object.

        Resturn
        -------
        str
            content of the input file
        """

        
        return """$$$
$ MODEL
{}
$ PROBLEM
{}
""".format(self.model._generate_jobdata(),
self.problem._generate_jobdata())



class SofistikParametersFile(ParametersFile):
    """Sofistik implementation of :class:`compas_fea2.job.input_file.ParametersFile`.\n
    """
    __doc__ += ParametersFile.__doc__

    def __init__(self, name=None, **kwargs):
        super(SofistikParametersFile, self).__init__(name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

