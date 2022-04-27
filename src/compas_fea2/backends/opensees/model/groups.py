from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model import NodesGroup
from compas_fea2.model import ElementsGroup
from compas_fea2.model.groups import FacesGroup, PartsGroup


class OpenseesNodesGroup(NodesGroup):
    """"""
    __doc__ += NodesGroup.__doc__

    def __init__(self, nodes, name=None, **kwargs):
        super(OpenseesNodesGroup, self).__init__(nodes=nodes, name=name, **kwargs)
        raise NotImplementedError


class OpenseesElementsGroup(ElementsGroup):
    """"""
    __doc__ += ElementsGroup.__doc__

    def __init__(self, *, elements, name=None, **kwargs):
        super(OpenseesElementsGroup, self).__init__(elements=elements, name=name, **kwargs)
        raise NotImplementedError


class OpenseesFacesGroup(FacesGroup):
    """Opensees implementation of the :class:`compas_fea2.model.FacesGroup`.\n
    """
    __doc__ += FacesGroup.__doc__

    def __init__(self, *, part, element_face, name=None, **kwargs):
        super(FacesGroup, self).__init__(part=part, element_face=element_face, name=name, **kwargs)
        raise NotImplementedError


class OpenseesPartsGroup(PartsGroup):
    """Opensees implementation of the :class:`compas_fea2.model.PartsGroup`.\n
    """
    __doc__ += PartsGroup.__doc__

    def __init__(self, *, parts, name=None, **kwargs):
        super(OpenseesPartsGroup, self).__init__(parts=parts, name=name, **kwargs)
        raise NotImplementedError
