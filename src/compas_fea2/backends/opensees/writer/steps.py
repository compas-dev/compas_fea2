
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

                # -------------------------------------------------------------------------------------------------
                # OpenSees
                # -------------------------------------------------------------------------------------------------

                if stype != 'ModalStep':

                    self.write_line('timeSeries Constant {0} -factor 1.0'.format(s_index))
                    self.write_line('pattern Plain {0} {0} -fact {1} {2}'.format(s_index, 1, '{'))
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

                    # -------------------------------------------------------------------------------------------------
                    # OpenSees
                    # -------------------------------------------------------------------------------------------------

                    # PointLoad
                    # ---------

                    if ltype == 'PointLoad':

                        compnents = ' '.join([str(com[dof] * fact) for dof in dofs[:self.ndof]])

                        for node in nodes:

                            ns = sets[node].selection if isinstance(node, str) else node

                            for ni in [i + 1 for i in ns]:
                                self.write_line('load {0} {1}'.format(ni, compnents))

                    # Gravity
                    # -------

                    elif ltype == 'GravityLoad':

                        for nkey, node in self.structure.nodes.items():

                            W = - fact * node.mass * 9.81
                            self.write_line('load {0} {1} {2} {3}'.format(nkey + 1, gx * W, gy * W, gz * W))

                    # LineLoad
                    # --------

                    elif ltype == 'LineLoad':

                        if axes == 'global':

                            raise NotImplementedError

                        elif axes == 'local':

                            elements = ' '.join([str(i + 1) for i in sets[k].selection])
                            lx = -com['x'] * fact
                            ly = -com['y'] * fact
                            self.write_line('eleLoad -ele {0} -type -beamUniform {1} {2}'.format(elements, ly, lx))

                    self.blank_line()

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

                    # -------------------------------------------------------------------------------------------------
                    # OpenSees
                    # -------------------------------------------------------------------------------------------------

                    for node in nodes:

                        ns = sets[node].selection if isinstance(node, str) else node

                        for ni in [i + 1 for i in ns]:

                            for c, dof in enumerate(dofs[:self.ndof], 1):
                                if com[dof] is not None:
                                    self.write_line('sp {0} {1} {2}'.format(ni, c, com[dof]))

                    self.blank_line()
                    self.blank_line()

            # =====================================================================================================
            # =====================================================================================================
            # OUTPUT
            # =====================================================================================================
            # =====================================================================================================

            self.write_subsection('Output')

            # -------------------------------------------------------------------------------------------------
            # OpenSees
            # -------------------------------------------------------------------------------------------------

            # Node recorders

            node_output = {
                'u':  '1 2 3 disp',
                'ur': '4 5 6 disp',
                'rf': '1 2 3 reaction',
                'rm': '4 5 6 reaction',
            }

            if stype != 'ModalStep':

                self.write_line('}')

                self.blank_line()
                self.write_subsection('Node recorders')

                prefix = 'recorder Node -file {0}{1}_'.format(temp, key)
                n = self.structure.node_count()

                for field in node_output:
                    if field in fields:
                        dof = node_output[field]
                        self.write_line('{0}{1}.out -time -nodeRange 1 {2} -dof {3}'.format(prefix, field, n, dof))
                        self.blank_line()

                # Sort elements

                truss_elements  = ''
                beam_elements   = ''
                spring_elements = ''
                truss_ekeys     = []
                beam_ekeys      = []
                spring_ekeys    = []

                for ekey, element in self.structure.elements.items():

                    eltype = element.__name__
                    n = '{0} '.format(ekey + 1)

                    if eltype == 'TrussElement':

                        truss_elements += n
                        truss_ekeys.append(ekey)

                    elif eltype == 'BeamElement':

                        beam_elements += n
                        beam_ekeys.append(ekey)

                    elif eltype == 'SpringElement':

                        spring_elements += n
                        spring_ekeys.append(ekey)

                # Element recorders

                self.blank_line()
                self.write_subsection('Element recorders')

                prefix = 'recorder Element -file {0}{1}_'.format(temp, key)

                if 'sf' in fields:

                    if truss_elements:
                        self.write_line('{0}sf_truss.out -time -ele {1} axialForce'.format(prefix, truss_elements))

                    if beam_elements:
                        self.write_line('{0}sf_beam.out -time -ele {1} localForce'.format(prefix, beam_elements))

                if 'spf' in fields:

                    if spring_elements:
                        self.write_line('{0}spf_spring.out -time -ele {1} basicForces'.format(prefix,
                                                                                                spring_elements))

                # ekeys

                with open('{0}truss_ekeys.json'.format(temp), 'w') as file:
                    json.dump({'truss_ekeys': truss_ekeys}, file)

                with open('{0}beam_ekeys.json'.format(temp), 'w') as file:
                    json.dump({'beam_ekeys': beam_ekeys}, file)

                with open('{0}spring_ekeys.json'.format(temp), 'w') as file:
                    json.dump({'spring_ekeys': spring_ekeys}, file)

                # Solver

                self.blank_line()
                self.write_subsection('Solver')
                self.blank_line()

                self.write_line('constraints Transformation')
                self.write_line('numberer RCM')
                self.write_line('system ProfileSPD')
                self.write_line('test NormUnbalance {0} {1} 5'.format(tolerance, iterations))
                self.write_line('algorithm NewtonLineSearch')
                self.write_line('integrator LoadControl {0}'.format(1. / increments))
                self.write_line('analysis Static')
                self.write_line('analyze {0}'.format(increments))

            else:

                self.blank_line()
                self.write_subsection('Node recorders')

                for mode in range(modes):
                    prefix = 'recorder Node -file {0}{1}_u_mode-{2}'.format(temp, key, mode + 1)
                    n = self.structure.node_count()
                    self.write_line('{0}.out -nodeRange 1 {1} -dof 1 2 3 "eigen {2}"'.format(prefix, n, mode + 1))
                    self.blank_line()

                self.write_subsection('Eigen analysis')

                self.write_line('set lambda [eigen {0}]'.format(modes))
                self.write_line('set omega {}')
                self.write_line('set f {}')
                self.write_line('set pi 3.141593')
                self.blank_line()
                self.write_line('foreach lam $lambda {')
                self.write_line('    lappend omega [expr sqrt($lam)]')
                self.write_line('    lappend f     [expr sqrt($lam)/(2*$pi)]')
                self.write_line('}')
                self.blank_line()
                self.write_line('puts "frequencies: $f"')
                self.blank_line()
                self.write_line('set file "{0}{1}_frequencies.txt"'.format(temp, key))
                self.write_line('set File [open $file "w"]')
                self.blank_line()
                self.write_line('foreach t $f {')
                self.write_line('    puts $File " $t"')
                self.write_line('}')
                self.write_line('close $File')
                self.blank_line()
                self.write_line('record')
