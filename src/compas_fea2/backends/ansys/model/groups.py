from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.groups import ElementsGroup
from compas_fea2.model.groups import FacesGroup
from compas_fea2.model.groups import NodesGroup
from compas_fea2.model.groups import PartsGroup


class AnsysElementsGroup(ElementsGroup):
    """ Ansys implementation of :class:`.ElementsGroup`.\n
    """
    __doc__ += ElementsGroup.__doc__

    def __init__(self, *, elements, name=None, **kwargs):
        super(AnsysElementsGroup, self).__init__(elements=elements, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysFacesGroup(FacesGroup):
    """ Ansys implementation of :class:`.FacesGroup`.\n
    """
    __doc__ += FacesGroup.__doc__

    def __init__(self, part, element_face, name=None, **kwargs):
        super(AnsysFacesGroup, self).__init__(part=part, element_face=element_face, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysNodesGroup(NodesGroup):
    """ Ansys implementation of :class:`.NodesGroup`.\n
    """
    __doc__ += NodesGroup.__doc__

    def __init__(self, *, nodes, name=None, **kwargs):
        super(AnsysNodesGroup, self).__init__(nodes=nodes, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError


class AnsysPartsGroup(PartsGroup):
    """ Ansys implementation of :class:`.PartsGroup`.\n
    """
    __doc__ += PartsGroup.__doc__

    def __init__(self, *, parts, name=None, **kwargs):
        super(AnsysPartsGroup, self).__init__(parts=parts, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError
