from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__all__ = [
    'Input',
]
class InputFile():

    def __init__(self, name, job_name, structure, path):
        self.name           = name
        self.job_name       = job_name
        self.heading="""** {}
*Heading
** Job name: {}
** Generated by: compas_fea2
*Preprint, echo=NO, history=NO, contact=NO
*PHYSICAL CONSTANTS, ABSOLUTE ZERO=-273.15, STEFAN BOLTZMANN=5.67e-8
**\n""".format(self.name, self.job_name)

        self.parts          = self._generate_part_section(self, structure)
        self.assembly       = self._generate_assembly_section(self, structure)
        self.materials      = self._generate_material_section(self, structure)
        self.int_props      = self._generate_int_props_section(self, structure)
        self.interactions   = self._generate_interactions_section(self, structure)
        self.bcs            = self._generate_bcs_section(self, structure)
        self.steps          = self._generate_steps_section(self, structure)

    # ==============================================================================
    # Constructor methods
    # ==============================================================================

    def _generate_part_section(self, structure, f):
        header = """** PARTS\n**\n"""
        section = [header]
        for part in structure.parts:
            section.append(part.keyword_start)
            section.append(part.data)
            section.append(part.keyword_end)
        return section

    def _generate_assembly_section(self, structure, f):
        header = """** ASSEMBLY\n**\n"""
        section = [header]
        section.append(structure.assembly.keyword_start)
        for instance in structure.assembly.instances:
            section.append(instance.data)
        for nset in structure.assembly.nsets:
            section.append(nset.data)
        for elset in structure.assembly.elsets:
            section.append(elset.data)
        for surface in structure.assembly.surfaces:
            section.append(surface.data)
        for constraint in structure.assembly.constraints:
            section.append(constraint.data)
        section.append(structure.assembly.keyword_end)

    def _generate_material_section(self, structure, f):
        header = """** MATERIALS\n**\n"""
        section = [header]
        for material in structure.assembly.materials:
            section.append(material.data)

    def _generate_int_props_section(self, structure):
        # # Write interaction properties
        # for interaction_property in self.interaction_properties:
        #     interaction_property.write_data_line(f)
        pass
    def _generate_interactions_section(self, structure):
        #
        # # Write interactions
        # for interaction in self.interactions:
        #     interaction.write_data_line(f)
        pass
    def _generate_bcs_section(self, structure):
        # # Write boundary conditions
        # for bc in self.bcs:
        #     bc.write_data(f)
        pass
    def _generate_steps_section(self, structure):
        # # Write steps
        # for step in self.steps:
        #     step.write_header(f)
        #     # Write loads
        #     for load in self.loads[step]:
        #         load.write_data_line(f)
        #     # Write Output Reequests
        #     for output in self.outputs[step]:
        #         output.write_data_line(f)
        #     step.write_keyword_end(f)
        pass

    def _generate_complete_file(self):
        return ''.join(self.heading, self.parts_header ,self.parts, self.assembly,
                       self.materials, self.int_props, self.interactions, self.bcs, self.steps)

    # ==============================================================================
    # General methods
    # ==============================================================================

    def write(self, file):
        with open(file, 'w') as f:
            f.writelines(self.complete)

