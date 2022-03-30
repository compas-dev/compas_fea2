from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import _Material
from compas_fea2.model import Concrete
from compas_fea2.model import ConcreteSmearedCrack
from compas_fea2.model import ConcreteDamagedPlasticity
from compas_fea2.model import ElasticIsotropic
from compas_fea2.model import Stiff
from compas_fea2.model import ElasticOrthotropic
from compas_fea2.model import ElasticPlastic
from compas_fea2.model import Steel


# ==============================================================================
# linear elastic
# ==============================================================================

class AbaqusElasticIsotropic(ElasticIsotropic):

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
        n = ''
        if self.unilateral:
            if self.unilateral == 'nc':
                n = '\n*NO COMPRESSION'
            elif self.unilateral == 'nt':
                n = '\n*NO TENSION'
            else:
                raise Exception(
                    'keyword {} for unilateral parameter not recognised. Please review the documentation'.format(self.unilateral))

        return ("*Material, name={}\n"
                "*Density\n"
                "{},\n"
                "*Elastic\n"
                "{}, {}{}\n").format(self.name, self.density, self.E, self.v, n)


# class AbaqusElasticOrthotropic(ElasticOrthotropic):
#     pass


# class AbaqusStiff(Stiff):

#     def _generate_jobdata(self):
#         """Generates the string information for the input file.

#         Parameters
#         ----------
#         None

#         Returns
#         -------
#         input file data line (str).
#         """
#         return ("*Material, name={}\n"
#                 "*Density\n"
#                 "{},\n"
#                 "*Elastic\n"
#                 "{}, {}\n").format(self.name, self.density, self.E['E'], self.v['v'])


# # ==============================================================================
# # non-linear general
# # ==============================================================================

# class AbaqusElasticPlastic(ElasticPlastic):

#     def __init__(self, E, v, density, f, e, name=None, **kwargs):
#         super(AbaqusElasticPlastic, self).__init__(E=E, v=v, density=density, f=f, e=e, name=name, **kwargs)

#     def _generate_jobdata(self):
#         """Generates the string information for the input file.

#         Parameters
#         ----------
#         None

#         Returns
#         -------
#         input file data line (str).
#         """
#         data_section = []
#         line = ("*Material, name={}\n"
#                 "*Density\n"
#                 "{},\n"
#                 "*Elastic\n"
#                 "{}, {}\n"
#                 "*Plastic").format(self.name, self.density, self.E['E'], self.v['v'])
#         data_section.append(line)

#         for i, j in zip(self.compression['f'], self.compression['e']):
#             line = """{}, {}""".format(abs(i), abs(j))
#             data_section.append(line)
#         return '\n'.join(data_section)


# # ==============================================================================
# # non-linear metal
# # ==============================================================================

# class AbaqusSteel(Steel):

#     def __init__(self, fy, fu, eu, E, v, density, name=None, **kwargs):
#         super(AbaqusSteel, self).__init__(name=name, fy=fy, fu=fu, eu=eu, E=E, v=v, density=density, name=name, **kwargs)

#     def _generate_jobdata(self):
#         """Generates the string information for the input file.

#         Parameters
#         ----------
#         None

#         Returns
#         -------
#         input file data line (str).
#         """
#         data_section = []
#         line = ("*Material, name={}\n"
#                 "*Density\n"
#                 "{},\n"
#                 "*Elastic\n"
#                 "{}, {}\n"
#                 "*Plastic").format(self.name, self.density, self.E['E'], self.v['v'])
#         data_section.append(line)

#         for i, j in zip(self.compression['f'], self.compression['e']):
#             line = """{}, {}""".format(abs(i), abs(j))
#             data_section.append(line)
#         return '\n'.join(data_section)


# # ==============================================================================
# # non-linear timber
# # ==============================================================================


# # ==============================================================================
# # non-linear masonry
# # ==============================================================================


# # ==============================================================================
# # non-linear concrete
# # ==============================================================================

# class AbaqusConcrete(Concrete):

#     def __init__(self, fck, v, density, fr, name=None, **kwargs):
#         super(AbaqusConcrete, self).__init__(fck=fck, v=v, density=density, fr=fr, name=name, **kwargs)

#     def _generate_jobdata(self):
#         """Generates the string information for the input file.

#         Parameters
#         ----------
#         None

#         Returns
#         -------
#         input file data line (str).
#         """
#         data_section = []
#         line = ("*Material, name={}\n"
#                 "*Density\n"
#                 "{},\n"
#                 "*Elastic\n"
#                 "{}, {}\n"
#                 "*Concrete\n").format(self.name, self.density, self.E['E'], self.v['v'])
#         data_section.append(line)

#         for i, j in zip(self.compression['f'], self.compression['e']):
#             line = """{}, {}""".format(abs(i), abs(j))
#             data_section.append(line)

#             data_section.append('*Tension stiffening')

#         for i, j in zip(self.tension['f'], self.tension['e']):
#             line = """{}, {}""".format(i, j)
#             data_section.append(line)

#         a, b = self.fratios
#         line = ("*Failure ratios\n"
#                 "{}, {}").format(a, b)
#         data_section.append(line)
#         return '\n'.join(data_section)


# class AbaqusConcreteSmearedCrack(ConcreteSmearedCrack):

#     def __init__(self, E, v, density, fc, ec, ft, et, fr, name=None, **kwargs):
#         super(AbaqusConcreteSmearedCrack, self).__init__(E=E, v=v, density=density,
#                                                          fc=fc, ec=ec, ft=ft, et=et, fr=fr, name=name, **kwargs)

#     def _generate_jobdata(self):
#         """Generates the string information for the input file.

#         Parameters
#         ----------
#         None

#         Returns
#         -------
#         input file data line (str).
#         """
#         data_section = []
#         line = ("*Material, name={}\n"
#                 "*Density\n"
#                 "{},\n"
#                 "*Elastic\n"
#                 "{}, {}\n"
#                 "*Concrete\n").format(self.name, self.density, self.E['E'], self.v['v'])
#         data_section.append(line)

#         for i, j in zip(self.compression['f'], self.compression['e']):
#             line = """{}, {}""".format(abs(i), abs(j))
#             data_section.append(line)

#             data_section.append('*Tension stiffening')

#         for i, j in zip(self.tension['f'], self.tension['e']):
#             line = """{}, {}""".format(i, j)
#             data_section.append(line)

#         a, b = self.fratios
#         line = ("*Failure ratios\n"
#                 "{}, {}").format(a, b)
#         data_section.append(line)
#         return '\n'.join(data_section)


# class AbaqusConcreteDamagedPlasticity(ConcreteDamagedPlasticity):

#     def __init__(self, E, v, density, damage, hardening, stiffening, name=None, **kwargs):
#         super(AbaqusConcreteDamagedPlasticity, self).__init__(E=E, v=v,
#                                                               density=density, damage=damage, hardening=hardening, stiffening=stiffening, name=name, **kwargs)

#     def _generate_jobdata(self):
#         """Generates the string information for the input file.

#         Parameters
#         ----------
#         None

#         Returns
#         -------
#         input file data line (str).
#         """
#         data_section = []
#         line = ("*Material, name={}\n"
#                 "*Density\n"
#                 "{},\n"
#                 "*Elastic\n"
#                 "{}, {}\n"
#                 "*Concrete Damaged Plasticity\n").format(self.name, self.density, self.E['E'], self.v['v'])
#         data_section.append(line)

#         data_section.append(', '.join([str(i) for i in self.damage]))
#         data_section.append('*CONCRETE COMPRESSION HARDENING')
#         for i in self.hardening:
#             data_section.append(', '.join([str(j) for j in i]))

#         data_section.append('*Concrete Tension Stiffening, type=GFI')
#         for i in self.stiffening:
#             data_section.append(', '.join([str(j) for j in i]))

#         return '\n'.join(data_section)


# # ==============================================================================
# # User-defined Materials
# # ==============================================================================


# class AbaqusUserMaterial(_Material):

#     """ User Defined Material (UMAT). Tho implement this type of material, a
#     separate subroutine is required

#     Parameters
#     ----------
#     name : str
#         Material name.
#     sub_path : str
#         Path to the subroutine (no spaces are allowed in the path!)
#     **kwars : var
#         constants needed for the UMAT definition (depends on the subroutine)
#     """

#     def __init__(self, sub_path, density=None, name=None, **kwargs):
#         _Material.__init__(self, name=name, **kwargs)

#         self.__name__ = 'UserMaterial'
#         self.__dict__.update(kwargs)
#         self._name = name
#         # os.path.abspath(os.path.join(os.path.dirname(__file__), "umat/Umat_hooke_iso.f")) #TODO find a way to deal with space in windows command line
#         self.sub_path = sub_path
#         self.desity = density
#         self.constants = self.get_constants()
#         # self.attr_list.extend(['E', 'v', 'G', 'p', 'path'])

#     def get_constants(self):
#         constants = []
#         for k in self.__dict__:
#             # TODO: I think we should we add constants in the list below?
#             if k not in ['__name__', 'name', 'attr_list', 'sub_path', 'p']:
#                 constants.append(self.__dict__[k])
#         return constants

#     def _generate_jobdata(self):
#         """Generates the string information for the input file.

#         Parameters
#         ----------
#         None

#         Returns
#         -------
#         input file data line (str).
#         """
#         k = [str(i) for i in self.constants]
#         return ("*Material, name={}\n"
#                 "*Density\n"
#                 "{},\n"
#                 "*User Material, constants={}\n"
#                 "{}").format(self.name, self.density, len(k), ', '.join(reversed(k)))
