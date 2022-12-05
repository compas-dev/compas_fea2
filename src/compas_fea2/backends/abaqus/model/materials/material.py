from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from compas_fea2.model import ElasticIsotropic
from compas_fea2.model import Stiff
from compas_fea2.model import ElasticOrthotropic
from compas_fea2.model import ElasticPlastic
from compas_fea2.model import UserMaterial


# ==============================================================================
# linear elastic
# ==============================================================================

class AbaqusElasticOrthotropic(ElasticOrthotropic):
    """Abaqus implementation of :class:`ElasticOrthotropic`\n"""
    __doc__ += ElasticOrthotropic.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Abaqus.

    """

    def __init__(self, *, Ex, Ey, Ez, vxy, vyz, vzx, Gxy, Gyz, Gzx, density, name=None, **kwargs):
        super(ElasticOrthotropic, self).__init__(Ex=Ex, Ey=Ey, Ez=Ez, vxy=vxy, vyz=vyz, vzx=vzx,
                                                 Gxy=Gxy, Gyz=Gyz, Gzx=Gzx, density=density, name=name, **kwargs)
        raise NotImplementedError


class AbaqusElasticIsotropic(ElasticIsotropic):
    """Abaqus implementation of :class:`ElasticIsotropic`\n"""
    __doc__ += ElasticIsotropic.__doc__

    def __init__(self, *, E, v, density, unilateral=None, name=None, **kwargs):
        super(AbaqusElasticIsotropic, self).__init__(E=E, v=v, density=density, name=name, **kwargs)
        self.unilateral = unilateral

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).

        """
        jobdata = ["*Material, name={}".format(self.name)]

        if self.density:
            jobdata.append("*Density\n{},".format(self.density))

        n = ''
        if self.unilateral:
            if self.unilateral == 'nc':
                n = '\n*NO COMPRESSION'
            elif self.unilateral == 'nt':
                n = '\n*NO TENSION'
            else:
                raise Exception(
                    'keyword {} for unilateral parameter not recognised. Please review the documentation'.format(self.unilateral))
        jobdata.append("*Elastic\n{}, {}{}".format(self.E, self.v, n))

        if self.expansion:
            jobdata.append("*Expansion\n{},".format(self.expansion))
        jobdata.append("**")
        return '\n'.join(jobdata)


class AbaqusStiff(Stiff):
    """Abaqus implementation of :class:`Stiff`\n"""
    __doc__ += Stiff.__doc__

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return ("*Material, name={}\n"
                "*Density\n"
                "{},\n"
                "*Elastic\n"
                "{}, {}\n"
                "**").format(self.name, self.density, self.E, self.v)


# ==============================================================================
# non-linear general
# ==============================================================================

class AbaqusElasticPlastic(ElasticPlastic):
    """Abaqus implementation of :class:`ElasticPlastic`\n"""
    __doc__ += ElasticPlastic.__doc__
    __doc__ += """
    Warning
    -------
    Currently not available in Abaqus.

    """

    def __init__(self, *, E, v, density, strain_stress, name=None, **kwargs):
        super(AbaqusElasticPlastic, self).__init__(E=E, v=v, density=density,
                                                   strain_stress=strain_stress, name=name, **kwargs)
        raise NotImplementedError
        self._e
        self._f

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
                "*Plastic").format(self.name, self.density, self.E['E'], self.v['v'])
        data_section.append(line)

        for i, j in zip(self.compression['f'], self.compression['e']):
            line = """{}, {}""".format(abs(i), abs(j))
            data_section.append(line)
        return '\n'.join(data_section)


# ==============================================================================
# User-defined Materials
# ==============================================================================


class AbaqusUserMaterial(UserMaterial):
    """Abaqus implementation of :class:`UserMaterial`\n"""
    __doc__ += UserMaterial.__doc__
    __doc__ += """ User Defined Material (UMAT).

    Tho implement this type of material, a separate subroutine is required.

    Parameters
    ----------
    name : str
        Material name.
    sub_path : str
        Path to the subroutine (no spaces are allowed in the path!)
    **kwars : var
        constants needed for the UMAT definition (depends on the subroutine)
    """

    def __init__(self, sub_path, density=None, name=None, **kwargs):
        super(AbaqusUserMaterial, self).__init__(self, name=name, **kwargs)

        self.__name__ = 'UserMaterial'
        self.__dict__.update(kwargs)
        self._name = name
        # os.path.abspath(os.path.join(os.path.dirname(__file__), "umat/Umat_hooke_iso.f")) #TODO find a way to deal with space in windows command line
        self.sub_path = sub_path
        self.desity = density
        self.constants = self.get_constants()
        # self.attr_list.extend(['E', 'v', 'G', 'p', 'path'])

    def get_constants(self):
        constants = []
        for k in self.__dict__:
            # TODO: I think we should we add constants in the list below?
            if k not in ['__name__', 'name', 'attr_list', 'sub_path', 'p']:
                constants.append(self.__dict__[k])
        return constants

    def _generate_jobdata(self):
        """Generates the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        k = [str(i) for i in self.constants]
        return ("*Material, name={}\n"
                "*Density\n"
                "{},\n"
                "*User Material, constants={}\n"
                "{}").format(self.name, self.density, len(k), ', '.join(reversed(k)))
