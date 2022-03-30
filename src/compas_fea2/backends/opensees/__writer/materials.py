
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# Author(s): Andrew Liew (github.com/andrewliew)


__all__ = [
    'Materials',
]

MPa = 10**(-6)
GPa = 10**(-9)


class Materials(object):

    def __init__(self):

        pass


    def write_materials(self):

        self.write_section('Materials')
        self.blank_line()

        materials = self.structure.materials

        for key, material in materials.items():

            self.write_subsection(key)

            mtype       = material.__name__
            m_index     = material.index + 1
            compression = getattr(material, 'compression', None)
            tension     = getattr(material, 'tension', None)
            E           = material.E
            G           = material.G
            v           = material.v
            p           = material.p

            # ------------------------------------------------------------------------------------------------------
            # OpenSees
            # ------------------------------------------------------------------------------------------------------

            # Elastic
            # -------

            if mtype == 'ElasticIsotropic':

                self.write_line('uniaxialMaterial Elastic {0} {1}'.format(m_index, E['E']))
                self.write_line('nDMaterial ElasticIsotropic {0} {1} {2} {3}'.format(
                                m_index + 1000, E['E'], v['v'], p))

            elif mtype == 'Steel':

                fy = material.fy
                fu = material.fu
                ep = material.ep
                EshE = (fu - fy) / ep

                self.write_line('uniaxialMaterial Steel01 {0} {1} {2} {3}'.format(m_index, fy, E['E'], EshE))

            self.blank_line()

        self.blank_line()
        self.blank_line()


# f.write('*CONDUCTIVITY\n')
# f.write('** k[W/mK]\n')
# f.write('**\n')

# for i in material.conductivity:
#     f.write(', '.join([str(j) for j in i]) + '\n')

# f.write('**\n')
# f.write('*SPECIFIC HEAT\n')
# f.write('** c[J/kgK]\n')
# f.write('**\n')

# for i in material.sheat:
#     f.write(', '.join([str(j) for j in i]) + '\n')
