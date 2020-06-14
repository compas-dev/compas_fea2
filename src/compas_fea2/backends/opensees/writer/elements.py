
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Author(s): Andrew Liew (github.com/andrewliew)


__all__ = [
    'Nodes',
    'Elements',
]


# abaqus_data = {
#     'AngleSection':       {'name': 'L',           'geometry': ['b', 'h', 't', 't']},
#     'BoxSection':         {'name': 'BOX',         'geometry': ['b', 'h', 'tw', 'tf', 'tw', 'tf']},
#     'CircularSection':    {'name': 'CIRC',        'geometry': ['r']},
#     'ISection':           {'name': 'I',           'geometry': ['c', 'h', 'b', 'b', 'tf', 'tf', 'tw']},
#     'PipeSection':        {'name': 'PIPE',        'geometry': ['r', 't']},
#     'RectangularSection': {'name': 'RECTANGULAR', 'geometry': ['b', 'h']},
#     'TrapezoidalSection': {'name': 'TRAPEZOID',   'geometry': ['b1', 'h', 'b2', 'c']},
#     'GeneralSection':     {'name': 'GENERAL',     'geometry': ['A', 'I11', 'I12', 'I22', 'J', 'g0', 'gw']},
#     'ShellSection':       {'name': None,          'geometry': ['t']},
#     'SolidSection':       {'name': None,          'geometry': None},
#     'TrussSection':       {'name': None,          'geometry': ['A']},
# }

class Nodes(object):

    def __init__(self):

        pass


    def write_nodes(self):

        self.write_section('Nodes')
        self.write_line('#')

        for key in sorted(self.structure.nodes, key=int):

            self.write_node(key)

        self.blank_line()
        for key in sorted(self.structure.nodes, key=int):
            if self.structure.nodes[key].mass:
                self.write_mass(key)

        self.blank_line()
        self.blank_line()


    def write_node(self, key):

        prefix  = 'node '
        spacer  = self.spacer
        x, y, z = self.structure.node_xyz(key)

        line    = '{0}{1}{2}{3:.3f}{2}{4:.3f}{2}{5:.3f}'.format(prefix, key + 1, spacer, x, y, z)
        self.write_line(line)


    def write_mass(self, key):

        mr = '' if self.ndof == 3 else '0 0 0'
        line = 'mass {0} {1} {1} {1} {2}'.format(key + 1, self.structure.nodes[key].mass, mr)
        self.write_line(line)


class Elements(object):

    def __init__(self):

        pass


    def write_elements(self):

        self.write_section('Elements')
        self.blank_line()

        elements   = self.structure.elements
        materials  = self.structure.materials
        properties = self.structure.element_properties
        sections   = self.structure.sections
        sets       = self.structure.sets

        written_springs = []

        for key in sorted(properties):

            self.write_subsection(key)

            property      = properties[key]
            reinforcement = property.rebar
            elset         = property.elset

            section       = sections[property.section]
            stype         = section.__name__
            geometry      = section.geometry
            material      = materials.get(property.material)

            if material:
                m_index = material.index + 1

            s_index = section.index + 1

            selection = property.elements if property.elements else sets[elset].selection

            if geometry is not None:

                t   = geometry.get('t', None)
                A   = geometry.get('A', None)
                J   = geometry.get('J', None)
                Ixx = geometry.get('Ixx', None)
                Iyy = geometry.get('Iyy', None)
                E   = material.E.get('E', None)
                G   = material.G.get('G', None)

            for select in selection:

                element = elements[select]
                nodes   = [str(i + 1) for i in element.nodes]
                no      = len(nodes)
                n       = select + 1
                ex      = element.axes.get('ex', None)
                ey      = element.axes.get('ey', None)
                ez      = element.axes.get('ez', None)


                # =====================================================================================================
                # =====================================================================================================
                # SOLID
                # =====================================================================================================
                # =====================================================================================================

                if stype == 'SolidSection':

                    # -------------------------------------------------------------------------------------------------
                    # OpenSees
                    # -------------------------------------------------------------------------------------------------

                    if len(nodes) == 4:

                        solid = 'FourNodeTetrahedron'
                        self.write_line('element {0} {1} {2} {3}'.format(solid, n, ' '.join(nodes), m_index + 1000))

                # =====================================================================================================
                # =====================================================================================================
                # SHELL
                # =====================================================================================================
                # =====================================================================================================

                elif stype == 'ShellSection':

                    # -------------------------------------------------------------------------------------------------
                    # OpenSees
                    # -------------------------------------------------------------------------------------------------

                    if no == 3:
                        self.write_line('element tri31 {0} {1} {2} PlaneStress {3} 0 {4} 0 0'.format(
                                        n, ' '.join(nodes), t, m_index + 1000, material.p))
                        # self.write_line('section PlateFiber {0} {1} {2}'.format(n, m_index + 1000, t))
                        # self.write_line('element ShellDKGT {0} {1} {0}'.format(n, ' '.join(nodes)))
                        # self.write_line('element ShellNLDKGT {0} {1} {0}'.format(n, ' '.join(nodes)))
                        # aparently unknown to OpenSees
                    else:
                        self.write_line('section PlateFiber {0} {1} {2}'.format(n, m_index + 1000, t))
                        self.write_line('element ShellNLDKGQ {0} {1} {0}'.format(n, ' '.join(nodes)))

                # =====================================================================================================
                # =====================================================================================================
                # TRUSS
                # =====================================================================================================
                # =====================================================================================================

                elif stype == 'TrussSection':

                    # -------------------------------------------------------------------------------------------------
                    # OpenSees
                    # -------------------------------------------------------------------------------------------------

                    e = 'element corotTruss'
                    self.write_line('{0} {1} {2} {3} {4} {5}'.format(e, n, nodes[0], nodes[1], A, m_index))

                # =====================================================================================================
                # =====================================================================================================
                # SPRING
                # =====================================================================================================
                # =====================================================================================================

                elif stype == 'SpringSection':

                    kx = section.stiffness.get('axial', 0)
                    ky = section.stiffness.get('lateral', 0)
                    kr = section.stiffness.get('rotation', 0)

                    # -------------------------------------------------------------------------------------------------
                    # OpenSees
                    # -------------------------------------------------------------------------------------------------



                    if s_index not in written_springs:

                        if kx:

                            self.write_line('uniaxialMaterial Elastic 2{0:0>3} {1}'.format(s_index, kx))
                            self.blank_line()

                        # else:
                        #     i = ' '.join([str(k) for k in section.forces['axial']])
                        #     j = ' '.join([str(k) for k in section.displacements['axial']])
                        #     f.write('uniaxialMaterial ElasticMultiLinear {0}01 -strain {1} -stress {2}\n'.format(
                        #         s_index, j, i))
                        #     f.write('#\n')

                        written_springs.append(s_index)

                    orientation = ' '.join([str(k) for k in ey])

                    self.write_line('element twoNodeLink {0} {1} {2} -mat 2{3:0>3} -dir 1 -orient {4}'.format(n, nodes[0], nodes[1], s_index, orientation))


                # =====================================================================================================
                # =====================================================================================================
                # MASS
                # =====================================================================================================
                # =====================================================================================================

                elif stype == 'MassSection':

                    # -------------------------------------------------------------------------------------------------
                    # OpenSees
                    # -------------------------------------------------------------------------------------------------

                    raise NotImplementedError


                # =====================================================================================================
                # =====================================================================================================
                # BEAM
                # =====================================================================================================
                # =====================================================================================================

                else:

                    # -------------------------------------------------------------------------------------------------
                    # OpenSees
                    # -------------------------------------------------------------------------------------------------

                    e = 'element elasticBeamColumn'
                    self.write_line('geomTransf Corotational {0} {1}'.format(n, ' '.join([str(i) for i in ex])))
                    self.write_line('{} {} {} {} {} {} {} {} {} {} {}'.format(e, n, nodes[0], nodes[1], A, E, G, J, Ixx, Iyy, n))

                self.blank_line()

            self.blank_line()
            self.blank_line()


