from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Author(s): Francesco Ranaudo (github.com/franaudo)

from compas_fea2.backends._base.model import ModelBase
from compas_fea2.backends.abaqus.model._instances import _Instance

__all__ = [
    'Model',
]


class Model(ModelBase):
    """ Abaqus Model object

    Note
    ----
    This is in many aspects equivalent to an `Assembly` in Abaqus.


    """
    __doc__ += ModelBase.__doc__

    def __init__(self, name, description=None, author=None):
        super(Model, self).__init__(name, description, author)
        self._backend = 'abaqus'
        self._instances = {}

    # =========================================================================
    #                             Parts methods
    # =========================================================================

    def add_part(self, part):
        """Adds a Part to the Model and creates an Instance object from the
        specified Part and adds it to the Assembly.

        Parameters
        ----------
        part : obj
            Part object from which the Instance is created.

        Returns
        -------
        None

        Examples
        --------
        >>> model = Assembly('mymodel')
        >>> part = Part('mypart')
        """
        super().add_part(part)
        self._add_instance(part)

    def remove_part(self, part):
        """ Removes the part from the Model and all the referenced instances
        of that part.

        Parameters
        ----------
        part : str
            Name of the Part to remove.

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

        Warning
        -------
        The creation of instances from the same part (which is a specific abaqus
        feature) is less useful in a scripting context (where it is easy to generate
        the parts already in their correct locations). Instances are created
        autmatically everytime a Part is added.

        Parameters
        ----------
        part : obj
            compas_fea2 Part object.

        Returns
        -------
        None
        """
        instance = _Instance(f'{part.name}-1', part)
        if instance.name not in self._instances:
            self._instances[instance.name] = instance
        else:
            print('Duplicate instance {} will be ignored!'.format(instance.name))

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

        self.instances.pop(instance)

    # =========================================================================
    #                            Groups methods
    # =========================================================================
    # NOTE in abaqus loads and bc must be applied to instance level sets, while sections
    # are applied to part level sets. Since in FEA2 there is no distinction,
    # this must be taken into account from the `add_group` method
    def add_group(self, group):
        '''Add a Group object to the Model at the instance level. Can be either
        a NodesGroup or an ElementsGroup.

        Parameters
        ----------
        group : obj
            group object.
        part : str
            Name of the part the group belongs to.

        Returns
        -------
        None
        '''
        super().add_group(group)

        if f'{group.part}-1' not in self._instances:
            raise ValueError(f'ERROR: instance {part}-1 not found in the Model!')
        self._instances[f'{group.part}-1'].add_group(group)
    # # =========================================================================
    # #                           BCs methods
    # # =========================================================================

    # def add_bc(self, bc, nodes, part):
    #     """Adds a boundary condition to the Problem object.

    #     Parameters
    #     ----------
    #     bc : obj
    #         `compas_fea2` BoundaryCondtion object.
    #     part : str
    #         part in the model where the BoundaryCondtion is applied.

    #     Returns
    #     -------
    #     None
    #     """
    #     super().add_bc(bc, nodes, part)
    #     self.add_group(bc.group, part)

    # def remove_bc(self, bc_name, part):
    #     raise NotImplementedError
# =============================================================================
#                               Job data
# =============================================================================

    def _generate_jobdata(self):
        return f"""**
** PARTS
**
{self._generate_part_section()}**
** MATERIALS
**
{self._generate_material_section()}**
** INTERACTION PROPERTIES
**
{self._generate_int_props_section()}**
** INTERACTIONS
**
{self._generate_interactions_section()}**
** ASSEMBLY
**
{self._generate_assembly_section()}**
** BOUNDARY CONDITIONS
**
{self._generate_bcs_section()}**
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
        for part in self.parts.values():
            data = part._generate_jobdata()
            data_section.append(data)
        return ''.join(data_section)

    def _generate_assembly_section(self):
        """Generate the content relatitive the assembly for the input file.

        Note
        ----
        in compas_fea2 the Model is for many aspects equivalent to an assembly in
        abaqus.

        Parameters
        ----------
        problem : obj
            compas_fea2 Problem object.

        Returns
        -------
        str
            text section for the input file.
        """
        data_section = ['*Assembly, name={}\n**\n'.format(self.name)]
        for instance in self._instances.values():
            data_section.append(instance._generate_jobdata())
            for group in instance.groups.values():
                data_section.append(group._generate_jobdata(instance.name))
            # for surface in self.surfaces:
            #     data_section.append(surface.jobdata)
        for constraint in self.constraints.values():
            data_section.append(constraint._generate_jobdata())
        data_section.append('*End Assembly\n**\n')

        return ''.join(data_section)

    def _generate_material_section(self):
        """Generate the content relatitive to the material section for the input
        file.

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
        for material in self.materials.values():
            data_section.append(material._generate_jobdata())
        return ''.join(data_section)

    def _generate_int_props_section(self):
        return ''

    def _generate_interactions_section(self):
        return ''

    def _generate_bcs_section(self):
        """Generate the content relatitive to the boundary conditions section
        for the input file.

        Parameters
        ----------
        problem : obj
            compas_fea2 Problem object.

        Returns
        -------
        str
            text section for the input file.
        """
        # # group elements by type and section
        # bctypes = set(map(lambda x: x.eltype, self.elements.values()))
        data_section = []
        for part in self.bcs:
            for node in self.bcs[part]:
                data_section += [bc._generate_jobdata(f'{part}-1', [node])
                                 for node, bc in self.bcs[part].items()]
        return '\n'.join(data_section)


# =============================================================================
#                               Debugging
# =============================================================================
if __name__ == "__main__":
    pass
