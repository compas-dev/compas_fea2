from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import _BeamEndRelease
from compas_fea2.model.releases import BeamEndPinRelease


# class AbaqusBeamEndRelease(_BeamEndRelease):
#     def __init__(self, element, location, n=False, v1=False, v2=False, m1=False, m2=False, t=False, name=None, **kwargs):
#         super(AbaqusBeamEndRelease).__init__(element, location, n=n,
#                                              v1=v1, v2=v2, m1=m1, m2=m2, t=t, name=name, **kwargs)


class AbaqusBeamEndPinRelease(BeamEndPinRelease):
    def __init__(self, m1=False, m2=False, t=False, name=None, **kwargs):
        super(AbaqusBeamEndPinRelease, self).__init__(m1=m1, m2=m2, t=t, name=name, **kwargs)

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        ends = {'start': 'S1', 'end': 'S2'}
        dofs = {'m1': 'M1', 'm2': 'M2', 't': 'T'}
        return '{},{},{}\n'.format(self.element.key, ends[self.location], ', '.join(dofs[dof] for dof in dofs if getattr(self, dof)))
