from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2 import config
from compas_fea2.model import Model
from compas_fea2.backends.abaqus.model._instances import _Instance
from compas_fea2.backends.abaqus.model.parts import AbaqusPart
from compas_fea2.utilities._utils import timer


class AbaqusModel(Model):
    """Abaqus implementation of a Model.

    Note
    ----
    For many aspects, in abaqus a `Model` is equivalent to an `Assembly`.
    """
    __doc__ += Model.__doc__

    def __init__(self, name=None, description=None, author=None, **kwargs):
        super(AbaqusModel, self).__init__(name=name, description=description, author=author, **kwargs)
        self._instances = set()

    # =========================================================================
    #                             Parts methods
    # =========================================================================

    def add_part(self, part):
        """Adds a Part to the Model and creates an Instance object from the
        specified Part and adds it to the Assembly.

        Parameters
        ----------
        part : :class:`compas_fea2.backends.abaus.model.parts.AbaqusPart`
            AbaqusPart object from which the Instance is created.

        Returns
        -------
        None
        """
        super().add_part(part)
        self._add_instance(part)
        return part

    def remove_part(self, part):
        """ Removes the part from the Model and all the referenced instances
        of that part.

        Parameters
        ----------
        part : :class:`compas_fea2.backends.abaus.model.parts.AbaqusPart`
            AbaqusPart object from which the Instance is created.

        Returns
        -------
        None
        """
        super().remove_part(part)
        self._remove_instance(part)

    # =========================================================================
    #                          Instances methods
    # =========================================================================

    def _add_instance(self, part):
        """Adds a compas_fea2 Instance of a Part object to the Model.

        Note
        ----
        The creation of instances from the same part (which is a specific abaqus
        feature) is less useful in a scripting context (where it is easy to generate
        the parts already in their correct locations). Instances are created
        autmatically everytime a Part is added.

        Note
        ----
        The name of the instance is automatically generated using abaqus convention
        of adding a "-1" to the name of the part from which it is generated.

        Parameters
        ----------
        part : :class:`compas_fea2.backends.abaus.model.parts.AbaqusPart`
            AbaqusPart object from which the Instance is created.

        Returns
        -------
        None
        """
        if not isinstance(part, AbaqusPart):
            raise TypeError("{!r} is not an abaqus part.".format(part))
        instance = _Instance(f'{part.name}-1', part)
        if instance in self._instances:
            if config.VERBOSE:
                print('Duplicate instance {} will be ignored!'.format(instance.name))
            return
        self._instances.add(instance)

    def _remove_instance(self, part):
        """ Removes the instance of a part from the Model.

        Parameters
        ----------
        part : str
            Name of the part object to remove.

        Returns
        -------
        None
        """

        raise NotImplementedError()
    # =========================================================================
    #                            Groups methods
    # =========================================================================

    def add_group(self, group, part):
        """Add a Group object to the Model at the instance level. Can be either
        a NodesGroup or an ElementsGroup.

        Note
        ----
        in abaqus loads and bc must be applied to instance level sets, while sections
        are applied to part level sets. Since in FEA2 there is no distinction,
        this is automatically taken into account from the `add_group` method

        Parameters
        ----------
        group : :class:`compas_fea2.model.Group`
            Group object to be added.

        Returns
        -------
        :class:`compas_fea2.model.Group`
        """
        super().add_group(group, part)
        if f'{part}-1' not in self._instances:
            raise ValueError(f'ERROR: instance {part}-1 not found in the Model!')
        self._instances[f'{part}-1'].add_group(group)

    def add_nodes_group(self, name, part, nodes):
        group = super().add_nodes_group(name, part, nodes)
        if f'{part}-1' not in self._instances:
            raise ValueError(f'ERROR: instance {part}-1 not found in the Model!')
        self._instances[f'{part}-1'].add_group(group.name)
        return group

    def add_elements_group(self, name, part, elements):
        group = super().add_elements_group(name, part, elements)
        if f'{part}-1' not in self._instances:
            raise ValueError(f'ERROR: instance {part}-1 not found in the Model!')
        self._instances[f'{part}-1'].add_group(group.name)
        return group

# =============================================================================
#                               Job data
# =============================================================================
    @timer(message='Model generated in ')
    def _generate_jobdata(self):
        return f"""**
** PARTS
**
{self._generate_part_section()}**
** ASSEMBLY
**
{self._generate_assembly_section()}**
** MATERIALS
**
{self._generate_material_section()}**
** INTERACTION PROPERTIES
**
{self._generate_int_props_section()}**
** INTERACTIONS
**
{self._generate_interactions_section()}**
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
        return ''.join(data_section)

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
        for instance in self._instances:
            data_section.append(instance._generate_jobdata())
            for group in instance.groups.values():
                data_section.append(group._generate_jobdata(instance.name))
        for facesgroup in self.facesgroups:
            data_section.append(facesgroup._generate_jobdata())
        for constraint in self.constraints:
            data_section.append(constraint._generate_jobdata())
        data_section.append('\n*End Assembly\n**\n')

        return ''.join(data_section)

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
        return ''.join(data_section)

    def _generate_int_props_section(self):
        data_section = []
        for interaction in self.interactions:
            data_section.append(interaction._generate_jobdata())
        return ''.join(data_section)

    def _generate_interactions_section(self):
        data_section = []
        for contact in self.contacts:
            data_section.append(contact._generate_jobdata())
        return ''.join(data_section)

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
