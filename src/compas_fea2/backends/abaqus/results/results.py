from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pathlib import Path
from re import L

from compas_fea2.results import Results, StepResults
from compas_fea2.backends.abaqus.results import odb_extract
from compas_fea2.utilities._utils import timer
from compas_fea2.utilities._utils import launch_process


class AbaqusResults(Results):
    """Abaqus implementation of :class:`Results`.\n"""
    __doc__ += Results.__doc__

    def __init__(self, database_name, database_path):
        super(AbaqusResults, self).__init__(database_name=database_name, database_path=database_path)



class AbaqusStepResults(StepResults):
    """Abaqus implementation of :class:`StepResults`.\n"""
    __doc__ += StepResults.__doc__

    def __init__(self, step, model):
        super(AbaqusStepResults, self).__init__(step, model)
