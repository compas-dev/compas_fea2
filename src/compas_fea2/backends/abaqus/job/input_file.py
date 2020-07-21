from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Author(s): Francesco Ranaudo (github.com/franaudo)

__all__ = [
    'InputFile',
]

class InputFile():

    def __init__(self, problem, filepath):
        self.name           = problem.name
        self.job_name       = problem.name
        self.filepath       = filepath

        self.parts          = self._generate_part_section(problem)
        self.assembly       = self._generate_assembly_section(problem)
        self.materials      = self._generate_material_section(problem)
        self.int_props      = self._generate_int_props_section(problem)
        self.interactions   = self._generate_interactions_section(problem)
        self.bcs            = self._generate_bcs_section(problem)
        self.steps          = self._generate_steps_section(problem)

        self.data           = self._generate_data()

    # ==============================================================================
    # Constructor methods
    # ==============================================================================

    def _generate_part_section(self, problem):
        section_data = []
        for part in problem.model.parts.values():
            data  = part._generate_data()
            section_data.append(data)
        return ''.join(section_data)

    def _generate_assembly_section(self, problem):
        return problem.model._generate_data()

    def _generate_material_section(self, problem):
        section_data = []
        for material in problem.model.materials.values():
            section_data.append(material.data)
        return ''.join(section_data)

    def _generate_int_props_section(self, problem):
        # # Write interaction properties
        # for interaction_property in problem.model.interaction_properties:
        #     interaction_property.write_data_line(f)
        return ''

    def _generate_interactions_section(self, problem):
        #
        # # Write interactions
        # for interaction in problem.model.interactions:
        #     interaction.write_data_line(f)
        return ''

    def _generate_bcs_section(self, problem):
        section_data = []
        for bc in problem.bcs.values():
            section_data.append(bc._generate_data())
        return ''.join(section_data)

    #TODO I need to loop through problem.STEP.loads
    def _generate_steps_section(self, problem):
        section_data = []
        for step in problem.steps:
            displacements = []
            for displacement in step.displacements:
                displacements.append(problem.displacements[displacement])
            loads = []
            for load in step.loads:
                loads.append(problem.loads[load])
            field_outputs = []
            for field_output in step.field_outputs:
                field_outputs.append(problem.field_outputs[field_output])
            history_outputs = []
            for history_output in step.history_outputs:
                history_outputs.append(problem.history_outputs[history_output])
            section_data.append(step._generate_data(displacements,
                                                    loads,
                                                    field_outputs,
                                                    history_outputs))
        return ''.join(section_data)

    def _generate_data(self):
        return """** {}
*Heading
** Job name: {}
** Generated by: compas_fea2
*PHYSICAL CONSTANTS, ABSOLUTE ZERO=-273.15, STEFAN BOLTZMANN=5.67e-8
**
** PARTS
**
{}**
** ASSEMBLY
**
{}
**
** MATERIALS
**
{}**
** INTERACTION PROPERTIES
**
{}**
** INTERACTIONS
**
{}**
** BOUNDARY
**
{}**
** STEPS
{}
""".format(self.name, self.job_name,self.parts, self.assembly, self.materials,
           self.int_props, self.interactions, self.bcs, self.steps)

    # ==============================================================================
    # General methods
    # ==============================================================================

    def write_to_file(self):
        with open(self.filepath, 'w') as f:
            f.writelines(self.data)


if __name__ == "__main__":
    pass
