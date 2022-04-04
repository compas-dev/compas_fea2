from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.model import Concrete
from compas_fea2.model import ConcreteSmearedCrack
from compas_fea2.model import ConcreteDamagedPlasticity

# ==============================================================================
# non-linear concrete
# ==============================================================================


class AbaqusConcrete(Concrete):
    """Abaqus implementation of :class:`Concrete`\n"""
    __doc__ += Concrete.__doc__

    def __init__(self, *, fck, v=0.2, density=2400, fr=None,  name=None, **kwargs):
        super(AbaqusConcrete, self).__init__(fck=fck, v=v, density=density, fr=fr, name=name, **kwargs)

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        data_section = []
        line = ("*Material, name={}\n"
                "*Density\n"
                "{},\n"
                "*Elastic\n"
                "{}, {}\n"
                "*Concrete\n").format(self.name, self.density, self.E['E'], self.v['v'])
        data_section.append(line)

        for i, j in zip(self.compression['f'], self.compression['e']):
            line = """{}, {}""".format(abs(i), abs(j))
            data_section.append(line)

            data_section.append('*Tension stiffening')

        for i, j in zip(self.tension['f'], self.tension['e']):
            line = """{}, {}""".format(i, j)
            data_section.append(line)

        a, b = self.fratios
        line = ("*Failure ratios\n"
                "{}, {}").format(a, b)
        data_section.append(line)
        return '\n'.join(data_section)


class AbaqusConcreteSmearedCrack(ConcreteSmearedCrack):
    """Abaqus implementation of :class:`ConcreteSmearedCrack`\n"""
    __doc__ += ConcreteSmearedCrack.__doc__

    def __init__(self, *, E, v, density, fc, ec, ft, et, fr=[1.16, 0.0836], name=None, **kwargs):
        super(AbaqusConcreteSmearedCrack, self).__init__(E=E, v=v, density=density,
                                                         fc=fc, ec=ec, ft=ft, et=et, fr=fr, name=name, **kwargs)

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        data_section = []
        line = ("*Material, name={}\n"
                "*Density\n"
                "{},\n"
                "*Elastic\n"
                "{}, {}\n"
                "*Concrete\n").format(self.name, self.density, self.E['E'], self.v['v'])
        data_section.append(line)

        for i, j in zip(self.compression['f'], self.compression['e']):
            line = """{}, {}""".format(abs(i), abs(j))
            data_section.append(line)

            data_section.append('*Tension stiffening')

        for i, j in zip(self.tension['f'], self.tension['e']):
            line = """{}, {}""".format(i, j)
            data_section.append(line)

        a, b = self.fratios
        line = ("*Failure ratios\n"
                "{}, {}").format(a, b)
        data_section.append(line)
        return '\n'.join(data_section)


class AbaqusConcreteDamagedPlasticity(ConcreteDamagedPlasticity):
    """Abaqus implementation of :class:`ConcreteDamagedPlasticity`\n"""
    __doc__ += ConcreteDamagedPlasticity.__doc__

    def __init__(self, *, E, v, density, damage, hardening, stiffening, name=None, **kwargs):
        super(AbaqusConcreteDamagedPlasticity, self).__init__(E=E, v=v,
                                                              density=density, damage=damage, hardening=hardening, stiffening=stiffening, name=name, **kwargs)

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        data_section = []
        line = ("*Material, name={}\n"
                "*Density\n"
                "{},\n"
                "*Elastic\n"
                "{}, {}\n"
                "*Concrete Damaged Plasticity\n").format(self.name, self.density, self.E['E'], self.v['v'])
        data_section.append(line)

        data_section.append(', '.join([str(i) for i in self.damage]))
        data_section.append('*CONCRETE COMPRESSION HARDENING')
        for i in self.hardening:
            data_section.append(', '.join([str(j) for j in i]))

        data_section.append('*Concrete Tension Stiffening, type=GFI')
        for i in self.stiffening:
            data_section.append(', '.join([str(j) for j in i]))

        return '\n'.join(data_section)
