from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import Part


class AbaqusPart(Part):
    """Abaqus implementation of :class:`Part`.
    """
    __doc__ += Part.__doc__

    def __init__(self, model=None, name=None, **kwargs):
        super(AbaqusPart, self).__init__(model=model, name=name, **kwargs)

    def _group_elements(self):
        """Group the elements. This is used internally to generate the input
        file.

        Parameters
        ----------
        None

        Returns
        -------
        dict
            {implementation:{section:{orientation: [elements]},},}
        """

        # group elements by type and section
        implementations = set(map(lambda x: x._implementation, self.elements))
        # group by type
        grouped_elements = {implementation: [
            el for el in self.elements if el._implementation == implementation] for implementation in implementations}
        # subgroup by section
        for implementation, elements in grouped_elements.items():
            sections = set(map(lambda x: x.section, elements))
            elements = {section: [el for el in elements if el.section == section] for section in sections}
            # subgroup by orientation
            for section, sub_elements in elements.items():
                orientations = set(map(lambda x: '_'.join(str(i) for i in x._orientation)
                                       if hasattr(x, '_orientation') else None, sub_elements))
                elements_by_orientation = {}
                for orientation in orientations:
                    elements_by_orientation.setdefault(orientation, set())
                    for el in sub_elements:
                        if hasattr(el, '_orientation'):
                            if '_'.join(str(i) for i in el._orientation) == orientation:
                                elements_by_orientation[orientation].add(el)
                        else:
                            elements_by_orientation[None].add(el)
                elements[section] = elements_by_orientation
            grouped_elements[implementation] = elements

        return grouped_elements

    # =========================================================================
    #                       Generate input file data
    # =========================================================================

    def _generate_jobdata(self):
        """Generate the string information for the input file.

        Parameters
        ----------
        None

        Returns
        -------
        str
            input file data lines.
        """
        return """**
*Part, name={}
**
** - Nodes
**   -----
{}
**
** - Elements
**   --------
{}
**
** - Sets
**   ----
{}
{}
**
** - Releases
**   --------
{}
**
*End Part""".format(self.name,
                    self._generate_nodes_section(),
                    self._generate_elements_section(),
                    self._generate_nodesets_section(),
                    self._generate_elementsets_section(),
                    self._generate_releases_section())

    def _generate_nodes_section(self):
        return '\n'.join(['*Node']+[node._generate_jobdata() for node in self.nodes])

    def _generate_elements_section(self):
        from compas_fea2.model import ElementsGroup
        part_data = []
        # Write elements, elsets and sections
        grouped_elements = self._group_elements()
        for implementation, sections in grouped_elements.items():
            for section, orientations in sections.items():
                for orientation, elements in orientations.items():
                    part_data.append("*Element, type={}".format(implementation))
                    # Write elements
                    for element in elements:
                        part_data.append(element._generate_jobdata())

                    # create and write aux set to assign the section
                    if orientation:
                        aux_elset = self.add_group(ElementsGroup(
                            name='aux_{}_{}_{}'.format(implementation, section.name, orientation.replace(".", "")),
                            elements=elements))
                        part_data.append(section._generate_jobdata(aux_elset.name, orientation.split('_')))
                    else:
                        aux_elset = self.add_group(ElementsGroup(
                            name='aux_{}_{}'.format(implementation, section.name),
                            elements=elements))
                        part_data.append(section._generate_jobdata(aux_elset.name))
        return '\n'.join(part_data)

    def _generate_nodesets_section(self):
        if self.nodesgroups:
            return '\n'.join([group._generate_jobdata() for group in self.nodesgroups])
        else:
            return '**'

    def _generate_elementsets_section(self):
        if self.elementsgroups:
            return '\n'.join([group._generate_jobdata() for group in self.elementsgroups])
        else:
            return '**'

    def _generate_releases_section(self):
        if self.releases:
            return '\n'.join(['*Release']+[release._generate_jobdata() for release in self.releases])
        else:
            return '**'

    def _generate_instance_jobdata(self):
        """Generates the string information for the input file.

        Note
        ----
        The creation of instances from the same part (which is a specific abaqus
        feature) is less useful in a scripting context (where it is easy to generate
        the parts already in their correct locations).

        Note
        ----
        The name of the instance is automatically generated using abaqus convention
        of adding a "-1" to the name of the part from which it is generated.

        Parameters
        ----------
        None

        Returns
        -------
        input file data line (str).
        """
        return '\n'.join(['*Instance, name={}-1, part={}'.format(self.name, self.name),
                          '*End Instance\n**'])
