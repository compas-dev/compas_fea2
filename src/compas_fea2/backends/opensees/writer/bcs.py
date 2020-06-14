
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# Author(s): Andrew Liew (github.com/andrewliew)


__all__ = [
    'BCs',
]

dofs    = ['x',  'y',  'z',  'xx', 'yy', 'zz']

# TODO remove this collection business
class BCs(object):

    def __init__(self):

        pass


    def write_boundary_conditions(self):

        self.write_section('Boundary conditions')
        self.blank_line()

        sets   = self.structure.sets
        steps         = self.structure.steps
        displacements = self.structure.displacements

        try:

            step = steps[self.structure.steps_order[0]]

            if isinstance(step.displacements, str):
                step.displacements = [step.displacements]

            for key in step.displacements:

                nodes      = displacements[key].nodes
                components = displacements[key].components
                nset       = nodes if isinstance(nodes, str) else None
                selection  = sets[nset].selection if isinstance(nodes, str) else nodes

                self.write_subsection(key)

                # ----------------------------------------------------------------------------
                # OpenSees
                # ----------------------------------------------------------------------------

                entry = ['1' if components[dof] is not None else '0' for dof in dofs[:self.ndof]]

                for node in sorted(selection, key=int):
                    self.write_line('fix {0} {1}'.format(node + 1, ' '.join(entry)))

        except:

            print('***** Error writing boundary conditions, check Step exists in structure.steps_order[0] *****')

        self.blank_line()
        self.blank_line()
