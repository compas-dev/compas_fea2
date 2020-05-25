
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import json


# Author(s): Andrew Liew (github.com/andrewliew)


__all__ = [
    'Steps',
]


dofs = ['x', 'y', 'z', 'xx', 'yy', 'zz']


class Steps(object):

    def __init__(self):

        pass


    def write_steps(self):

        self.write_section('Steps')
        self.blank_line()

        displacements = self.structure.displacements
        loads         = self.structure.loads
        steps         = self.structure.steps
        sets          = self.structure.sets
        fields        = self.fields

        # temp folder

        temp = '{0}{1}/'.format(self.structure.path, self.structure.name)

        try:
            os.stat(temp)
            for file in os.listdir(temp):
                os.remove(os.path.join(temp, file))
        except:
            os.mkdir(temp)

        # Steps

        for key in self.structure.steps_order[1:]:

            step       = steps[key]
            stype      = step.__name__
            s_index    = step.index
            factor     = getattr(step, 'factor', 1)
            increments = getattr(step, 'increments', 100)
            iterations = getattr(step, 'iterations', 100)
            tolerance  = getattr(step, 'tolerance', None)
            method     = getattr(step, 'type')
            modes      = getattr(step, 'modes', None)
            modify     = getattr(step, 'modify', None)
            nlgeom     = 'YES' if getattr(step, 'nlgeom', None) else 'NO'
            op         = 'MOD' if modify else 'NEW'


            # =====================================================================================================
            # =====================================================================================================
            # HEADER
            # =====================================================================================================
            # =====================================================================================================

            if stype in ['GeneralStep', 'BucklingStep', 'ModalStep']:

                self.write_subsection(key)


                if stype == 'ModalStep':

                    self.write_line('*STEP, NAME={0}'.format(key))
                    self.write_line('*FREQUENCY, EIGENSOLVER=LANCZOS, NORMALIZATION=DISPLACEMENT')
                    self.write_line('{0}'.format(modes))

                else:

                    p = ', PERTURBATION' if stype == 'BucklingStep' else ''
                    self.write_line('*STEP, NLGEOM={0}, NAME={1}{2}, INC={3}'.format(nlgeom, key, p, increments))
                    self.blank_line()
                    self.write_line('*{0}'.format(method.upper()))
                    self.blank_line()

                    if stype == 'BucklingStep':
                        self.write_line('{0}, {1}, {2}, {3}'.format(modes, modes, 5 * modes, increments))

                self.blank_line()

            # =====================================================================================================
            # =====================================================================================================
            # LOADS
            # =====================================================================================================
            # =====================================================================================================

            if getattr(step, 'loads', None):

                if isinstance(step.loads, str):
                    step.loads = [step.loads]

                for k in step.loads:

                    self.write_subsection(k)

                    load  = loads[k]
                    ltype = load.__name__
                    com   = getattr(load, 'components', None)
                    axes  = getattr(load, 'axes', None)
                    nodes = getattr(load, 'nodes', None)
                    fact  = factor.get(k, 1.0) if isinstance(factor, dict) else factor

                    if com:
                        gx = com.get('x', 0)
                        gy = com.get('y', 0)
                        gz = com.get('z', 0)

                    if isinstance(nodes, str):
                        nodes = [nodes]

                    if isinstance(load.elements, str):
                        elements = [load.elements]
                    else:
                        elements = load.elements


                    # PointLoad
                    # ---------

                    if ltype == 'PointLoad':

                        self.write_line('*LoadBase, OP={0}'.format(op))
                        self.blank_line()

                        for node in nodes:

                            ni = node if isinstance(node, str) else node + 1

                            for c, dof in enumerate(dofs, 1):
                                if com[dof]:
                                    self.write_line('{0}, {1}, {2}'.format(ni, c, com[dof] * fact))

                    # AreaLoad
                    # --------

                    elif ltype == 'AreaLoad':

                        for k in elements:
                            self.write_line('*DLOAD, OP={0}'.format(op))
                            self.blank_line()

                            if com['z']:
                                self.write_line('{0}, P, {1}'.format(k, fact * com['z']))
                                self.blank_line()

                    # PointLoads
                    # ----------

                    elif ltype == 'PointLoads':
                        self.write_line('*LoadBase, OP={0}'.format(op))
                        self.blank_line()

                        for node, coms in com.items():
                            for ci, value in coms.items():
                                index = dofs.index(ci) + 1
                                self.write_line('{0}, {1}, {2}'.format(node + 1, index, value * fact))

                    # Gravity
                    # -------

                    elif ltype == 'GravityLoad':

                        for k in elements:

                            self.write_line('*DLOAD, OP={0}'.format(op))
                            self.blank_line()
                            self.write_line('{0}, GRAV, {1}, {2}, {3}, {4}'.format(k, -9.81 * fact, gx, gy, gz))
                            self.blank_line()

                    # TributaryLoad
                    # -------------

                    elif ltype == 'TributaryLoad':

                        self.write_line('*LoadBase, OP={0}'.format(op))
                        self.blank_line()

                        for node in sorted(com, key=int):

                            ni = node + 1

                            for ci, dof in enumerate(dofs[:3], 1):
                                if com[node][dof]:
                                    self.write_line('{0}, {1}, {2}'.format(ni, ci, com[node][dof] * fact))

                    # LineLoad
                    # --------

                    elif ltype == 'LineLoad':

                        for k in elements:

                            self.write_line('*DLOAD, OP={0}'.format(op))
                            self.blank_line()

                            if axes == 'global':

                                for dof in dofs[:3]:
                                    if com[dof]:
                                        self.write_line('{0}, P{1}, {2}'.format(k, dof.upper(), fact * com[dof]))

                            elif axes == 'local':

                                if com['x']:
                                    self.write_line('{0}, P1, {1}'.format(k, fact * com['x']))

                                if com['y']:
                                    self.write_line('{0}, P2, {1}'.format(k, fact * com['y']))

                    # Prestress
                    # ---------

                    elif ltype == 'PrestressLoad':

                        for k in elements:

                            stresses = ''

                            if com['sxx']:
                                stresses += str(com['sxx'] * fact)

                            self.write_line('*INITIAL CONDITIONS, TYPE=STRESS')
                            self.blank_line()
                            self.write_line('{0}, {1}'.format(k, stresses))

                self.blank_line()
                self.blank_line()


            # =====================================================================================================
            # =====================================================================================================
            # DISPLACEMENTS
            # =====================================================================================================
            # =====================================================================================================

            if getattr(step, 'displacements', None):

                if isinstance(step.displacements, str):
                    step.displacements = [step.displacements]

                for k in step.displacements:

                    displacement = displacements[k]
                    com          = displacement.components
                    nodes        = displacement.nodes

                    if isinstance(nodes, str):
                        nodes = [nodes]

                    fact = factor.get(k, 1.0) if isinstance(factor, dict) else factor

                    if stype not in ['ModalStep', 'BucklingStep']:

                        self.write_line('*BOUNDARY')
                        self.blank_line()

                        for node in nodes:

                            ni = node if isinstance(node, str) else node + 1

                            for c, dof in enumerate(dofs, 1):
                                if com[dof] is not None:
                                    self.write_line('{0}, {1}, {1}, {2}'.format(ni, c, com[dof] * fact))

                        self.blank_line()
                        self.blank_line()


            # =====================================================================================================
            # =====================================================================================================
            # OUTPUT
            # =====================================================================================================
            # =====================================================================================================

            self.write_subsection('Output')


            node_fields    = ['rf', 'rm', 'u', 'ur', 'cf', 'cm']
            element_fields = ['sf', 'sm', 'sk', 'se', 's', 'e', 'pe', 'rbfor', 'ctf']

            if 'spf' in fields:
                fields[fields.index('spf')] = 'ctf'

            self.write_line('*OUTPUT, FIELD')
            self.blank_line()
            self.write_line('*NODE OUTPUT')
            self.blank_line()
            self.write_line(', '.join([i.upper() for i in node_fields if i in fields]))
            self.blank_line()
            self.write_line('*ELEMENT OUTPUT')
            self.blank_line()
            self.write_line(', '.join([i.upper() for i in element_fields if (i in fields and i != 'rbfor')]))

            if 'rbfor' in fields:
                self.write_line('*ELEMENT OUTPUT, REBAR')
                self.write_line('RBFOR')

            self.blank_line()
            self.write_line('*END STEP')
            self.blank_line()
            self.blank_line()



# Thermal

# try:
#     duration = step.duration
# except:
#     duration = 1
#     temperatures = steps[key].temperatures
#     if temperatures:
#         file = misc[temperatures].file
#         einc = str(misc[temperatures].einc)
#         f.write('**\n')
#         f.write('*TEMPERATURE, FILE={0}, BSTEP=1, BINC=1, ESTEP=1, EINC={1}, INTERPOLATE\n'.format(file, einc))

# elif stype == 'HeatStep':

#     temp0 = step.temp0
#     duration = step.duration
#     deltmx = steps[key].deltmx
#     interaction = interactions[step.interaction]
#     amplitude = interaction.amplitude
#     interface = interaction.interface
#     sink_t = interaction.sink_t
#     film_c = interaction.film_c
#     ambient_t = interaction.ambient_t
#     emissivity = interaction.emissivity

#     # Initial T

#     f.write('*INITIAL CONDITIONS, TYPE=TEMPERATURE\n')
#     f.write('NSET_ALL, {0}\n'.format(temp0))
#     f.write('**\n')

#     # Interface

#     f.write('*STEP, NAME={0}, INC={1}\n'.format(sname, increments))
#     f.write('*{0}, END=PERIOD, DELTMX={1}\n'.format(method, deltmx))
#     f.write('1, {0}, 5.4e-05, {0}\n'.format(duration))
#     f.write('**\n')
#     f.write('*SFILM, AMPLITUDE={0}\n'.format(amplitude))
#     f.write('{0}, F, {1}, {2}\n'.format(interface, sink_t, film_c))
#     f.write('**\n')
#     f.write('*SRADIATE, AMPLITUDE={0}\n'.format(amplitude))
#     f.write('{0}, R, {1}, {2}\n'.format(interface, ambient_t, emissivity))

#     # fieldOutputs

#     f.write('**\n')
#     f.write('** OUTPUT\n')
#     f.write('** ------\n')
#     f.write('*OUTPUT, FIELD\n')
#     f.write('**\n')
#     f.write('*NODE OUTPUT\n')
#     f.write('NT\n')
#     f.write('**\n')
#     f.write('*END STEP\n')