from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import DeformablePart, RigidPart


def _generate_jobdata(obj):
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
*End Part""".format(obj.name,
                    _generate_nodes_section(obj),
                    _generate_elements_section(obj) or '**',
                    _generate_nodesets_section(obj) or '**',
                    _generate_elementsets_section(obj) or '**',
                    _generate_releases_section(obj) or '**')


def _generate_nodes_section(obj):
    return '\n'.join(['*Node']+[node._generate_jobdata() for node in obj.nodes])


def _generate_elements_section(obj):
    part_data = []
    # Write elements, elsets and sections
    # this check is needed for rigid parts ->ugly, change!
    grouped_elements = obj._group_elements()
    if not isinstance(obj, RigidPart):
        for implementation, sections in grouped_elements.items():
            for section, orientations in sections.items():
                for orientation, elements in orientations.items():
                    # Write elements
                    elset_name = 'aux_{}_{}'.format(implementation, section.name)
                    if orientation:
                        elset_name += '_{}'.format(orientation.replace(".", ""))
                        orientation = orientation.split('_')
                    part_data.append("*Element, type={}, elset={}".format(implementation, elset_name))
                    for element in elements:
                        part_data.append(element._generate_jobdata())
                    part_data.append(section._generate_jobdata(elset_name, orientation=orientation))
    else:
        for implementation, elements in grouped_elements.items():
            elset_name = 'aux_{}'.format(implementation)
            part_data.append("*Element, type={}, elset={}".format(implementation, elset_name))
            for element in elements:
                part_data.append(element._generate_jobdata())
    return '\n'.join(part_data)


def _generate_nodesets_section(obj):
    if obj.nodesgroups:
        return '\n'.join([group._generate_jobdata() for group in obj.nodesgroups])
    else:
        return '**'


def _generate_elementsets_section(obj):
    if obj.elementsgroups:
        return '\n'.join([group._generate_jobdata() for group in obj.elementsgroups])
    else:
        return '**'


def _generate_releases_section(obj):
    if isinstance(obj, DeformablePart):
        if obj.releases:
            return '\n'.join(['*Release']+[release._generate_jobdata() for release in obj.releases])
    else:
        return '**'


def _generate_instance_jobdata(obj):
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
    return '\n'.join(['*Instance, name={}-1, part={}'.format(obj.name, obj.name),
                      '*End Instance\n**'])


class AbaqusDeformablePart(DeformablePart):
    """Abaqus implementation of :class:`DeformablePart`.
    """
    __doc__ += DeformablePart.__doc__

    def __init__(self, name=None, **kwargs):
        super(AbaqusDeformablePart, self).__init__(name=name, **kwargs)

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
        return _generate_jobdata(self)

    def _generate_instance_jobdata(self):
        return _generate_instance_jobdata(self)


class AbaqusRigidPart(RigidPart):
    def __init__(self, name=None, **kwargs):
        super(AbaqusRigidPart, self).__init__(name=name, **kwargs)

    # =========================================================================
    #                       Generate input file data
    # =========================================================================

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
            grouped_elements[implementation] = elements

        return grouped_elements

    def _generate_jobdata(self):
        return _generate_jobdata(self)

    def _generate_rigid_body_jobdata(self):
        return "*Rigid Body, ref node={0}-1.ref_point, elset={0}-1.all_elements".format(self.name)

    def _generate_instance_jobdata(self):
        return _generate_instance_jobdata(self)
