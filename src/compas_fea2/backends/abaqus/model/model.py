from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import Model
from compas_fea2.utilities._utils import timer


class AbaqusModel(Model):
    """Abaqus implementation of :class:`Model`.

    Note
    ----
    For many aspects, this is equivalent to an `Assembly` in Abaqus.

    """
    __doc__ += Model.__doc__

    def __init__(self, name=None, description=None, author=None, **kwargs):
        super(AbaqusModel, self).__init__(name=name, description=description, author=author, **kwargs)


# =============================================================================
#                               Job data
# =============================================================================

    @timer(message='Model generated in ')
    def _generate_jobdata(self):
        return f"""**
** PARTS
**
{self._generate_part_section()}
**
** ASSEMBLY
**
{self._generate_assembly_section()}
**
** MATERIALS
**
{self._generate_material_section()}
**
** INTERACTIONS
**
{self._generate_interactions_section()}
**
** INTERFACES
**
{self._generate_interfaces_section()}
**
** INITIAL CONDITIONS
**
{self._generate_bcs_section()}
"""

    def _generate_part_section(self):
        """Generate the content relatitive the each Part for the input file.

        Parameters
        ----------
        problem : obj
            compas_fea2 Problem object.

        Returns
        -------
        str
            text section for the input file.
        """
        data_section = []
        for part in self.parts:
            data = part._generate_jobdata()
            data_section.append(data)
        return '\n'.join(data_section)

    def _generate_assembly_section(self):
        """Generate the content relatitive the assembly for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        str
            text section for the input file.
        """
        data_section = ['*Assembly, name={}\n**\n'.format(self.name)]
        for part in self._parts:
            data_section.append(part._generate_instance_jobdata())
            for group in part.nodesgroups:
                data_section.append(group._generate_jobdata(instance=True))
            for group in part.elementsgroups:
                data_section.append(group._generate_jobdata(instance=True))
            for group in part.facesgroups:
                data_section.append(group._generate_jobdata())
        for constraint in self.constraints:
            data_section.append(constraint._generate_jobdata())
        data_section.append('*End Assembly')

        return '\n'.join(data_section)

    def _generate_material_section(self):
        """Generate the content relatitive to the material section for the input
        file.

        Parameters
        ----------
        None

        Returns
        -------
        str
            text section for the input file.
        """
        data_section = []
        materials = set()
        for part in self.parts:
            for material in part.materials:
                materials.add(material)
        for material in materials:
            data_section.append(material._generate_jobdata())
        return '\n'.join(data_section)

    def _generate_interactions_section(self):
        return '\n'.join(interaction._generate_jobdata() for interaction in self.interactions) if self.interactions else '**'

    def _generate_interfaces_section(self):
        return '\n'.join(interface._generate_jobdata() for interface in self.interfaces) if self.interfaces else '**'

    def _generate_bcs_section(self):
        """Generate the content relatitive to the boundary conditions section
        for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        str
            text section for the input file.
        """
        data_section = []
        for part in self.bcs:
            data_section += [bc._generate_jobdata('{}-1'.format(part.name), nodes)
                             for bc, nodes in self.bcs[part].items()]
        return '\n'.join(data_section)
