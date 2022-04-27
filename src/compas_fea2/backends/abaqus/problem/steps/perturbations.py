from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.problem.steps import ModalAnalysis
from compas_fea2.problem.steps import BucklingAnalysis
from compas_fea2.problem.steps import ComplexEigenValue
from compas_fea2.problem.steps import LinearStaticPerturbation
from compas_fea2.problem.steps import StedyStateDynamic
from compas_fea2.problem.steps import SubstructureGeneration


def _generate_jobdata(obj):
    """Generates the string information for the input file.

    Parameters
    ----------
    obj :

    Returns
    -------
    input file data line (str).
    """
    return """** ----------------------------------------------------------------
**
** STEP: {0}
**
* Step, name={0}, nlgeom={1}, perturbation
*{2}
**\n""".format(obj.name, obj.nlgeom, obj.stype)


class AbaqusModalAnalysis(ModalAnalysis):
    """"""
    __doc__ += ModalAnalysis.__doc__

    def __init__(self, modes=1, name=None, **kwargs):
        super(AbaqusModalAnalysis, self).__init__(modes, name=name, **kwargs)

    def _generate_jobdata(self):
        """Generates the string information for the input file.

       Parameters
        ----------
        None

        Returns
        -------
        input file data line(str).
        """
        return ("** ----------------------------------------------------------------\n"
                "**\n"
                "** STEP: {0}\n"
                "**\n"
                "*Step, name={0}\n"
                "*FREQUENCY, EIGENSOLVER=LANCZOS, NORMALIZATION=DISPLACEMENT\n"
                "{1}\n"
                "*End Step").format(self.name, self.modes)


class AbaqusComplexEigenValue(ComplexEigenValue):
    def __init__(self, name=None, **kwargs):
        super(AbaqusComplexEigenValue, self).__init__(name, **kwargs)
        raise NotImplementedError


class AbaqusBucklingAnalysis(BucklingAnalysis):
    """Initialises BuckleStep object for use in a buckling analysis.

    Parameters
    ----------
    name : str
        Name of the GeneralStep.
    displacements : list
        Displacement objects.
    loads : list
        Load objects.
    """

    def __init__(self, name=None, **kwargs):
        super(AbaqusBucklingAnalysis, self).__init__(name, **kwargs)
        self._nlgeom = 'NO'  # BUG this depends on the previous step -> loop through the steps order and adjust this parameter
        self._stype = 'Buckle'

    def _generate_jobdata(self):
        return _generate_jobdata(self)


class AbaqusLinearStaticPerturbation(LinearStaticPerturbation):
    """Initialises the StaticLinearPertubationStep object for use in a static analysis.

    Parameters
    ----------
    name : str
        Name of the GeneralStep.
    displacements : list
        Displacement objects.
    loads : list
        Load objects.

   """
    __doc__ += LinearStaticPerturbation.__doc__

    def __init__(self, name=None, **kwargs):
        super(AbaqusLinearStaticPerturbation, self).__init__(name=name, **kwargs)

        # BUG this depends on the previous step -> loop through the steps order and adjust this parameter
        self._nlgeom = 'NO'  # if not nlgeom else 'YES'
        self._stype = 'Static'

    def _generate_jobdata(self):
        return _generate_jobdata(self)


class AbaqusStedyStateDynamic(StedyStateDynamic):
    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        raise NotImplementedError


class AbaqusSubstructureGeneration(SubstructureGeneration):
    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        raise NotImplementedError
