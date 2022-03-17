from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import Part


class AbaqusPart(Part):
    """Initialises a ``Part`` object.

    Parameters
    ----------
    name : str
        Name of the ``Part``.

    """
    __doc__ += Part.__doc__

    def __init__(self, name):
        super(AbaqusPart, self).__init__(name)

    def _group_elements(self):
        """Group the elements. This is used internally to generate the input
        file.

        Parameters
        ----------
        None

        Returns
        -------
        dict
            {eltype:{section:{orientation: [elements]},},}
        """

        # group elements by type and section
        eltypes = set(map(lambda x: x.eltype, self.elements.values()))
        # group by type
        grouped_elements = {eltype: [el for el in self.elements.values() if el.eltype == eltype] for eltype in eltypes}
        # subgroup by section
        for eltype, elements in grouped_elements.items():
            sections = set(map(lambda x: x.section, elements))
            elements = {section: [el for el in elements if el.section == section] for section in sections}
            # subgroup by orientation
            for section, sub_elements in elements.items():
                orientations = set(map(lambda x: '_'.join(str(i) for i in x.orientation)
                                       if hasattr(x, 'orientation') else None, sub_elements))
                elements_by_orientation = {}
                for orientation in orientations:
                    elements_by_orientation.setdefault(orientation, set())
                    for el in sub_elements:
                        if hasattr(el, 'orientation'):
                            if '_'.join(str(i) for i in el.orientation) == orientation:
                                elements_by_orientation[orientation].add(el)
                        else:
                            elements_by_orientation[None].add(el)
                elements[section] = elements_by_orientation
            grouped_elements[eltype] = elements

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
        from compas_fea2.backends.abaqus.model import ElementsGroup
        # Write nodes
        part_data = ['*Node\n']
        for node in self.nodes:
            part_data.append(node._generate_jobdata())

        # Write elements, elsets and sections
        grouped_elements = self._group_elements()
        for eltype, sections in grouped_elements.items():
            for section, orientations in sections.items():
                for orientation, elements in orientations.items():
                    part_data.append("*Element, type={}\n".format(eltype))
                    # Write elements
                    for element in elements:
                        part_data.append(element._generate_jobdata())

                    # create and write aux set to assign the section
                    selection = [element.key for element in elements]
                    selection.sort()
                    if orientation:
                        aux_elset = ElementsGroup(
                            f'aux_{eltype}_{section.name}_{orientation.replace(".", "")}', selection)
                        self.add_group(aux_elset)
                        part_data.append(aux_elset._generate_jobdata())
                        # Write section
                        part_data.append(section._generate_jobdata(aux_elset.name, orientation.split('_')))
                    else:
                        aux_elset = ElementsGroup(f'aux_{eltype}_{section.name}', selection)
                        self.add_group(aux_elset)
                        part_data.append(aux_elset._generate_jobdata())
                        part_data.append(section._generate_jobdata(aux_elset.name))

        # Write user-defined groups
        for group in self.groups.values():
            part_data.append(group._generate_jobdata())

        # Write releases
        if self.releases:
            part_data.append('\n*Release\n')
            for release in self.releases:
                part_data.append(release._generate_jobdata())

        temp = ''.join(part_data)
        return ''.join(["*Part, name={}\n".format(self.name), temp,
                        "*End Part\n**\n"])
