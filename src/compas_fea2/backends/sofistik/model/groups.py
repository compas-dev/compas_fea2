from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2.model.groups import ElementsGroup
from compas_fea2.model.groups import FacesGroup
from compas_fea2.model.groups import NodesGroup
from compas_fea2.model.groups import PartsGroup

class SofistikElementsGroup(ElementsGroup):
    """Sofistik implementation of :class:`compas_fea2.model.groups.ElementsGroup`.\n
    """
    __doc__ += ElementsGroup.__doc__

    def __init__(self, *, elements, name=None, **kwargs):
        super(SofistikElementsGroup, self).__init__(elements=elements, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikFacesGroup(FacesGroup):
    """Sofistik implementation of :class:`compas_fea2.model.groups.FacesGroup`.\n
    """
    __doc__ += FacesGroup.__doc__

    def __init__(self, *, faces, name=None, **kwargs):
        super(SofistikFacesGroup, self).__init__(faces=faces, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikNodesGroup(NodesGroup):
    """Sofistik implementation of :class:`compas_fea2.model.groups.NodesGroup`.\n
    """
    __doc__ += NodesGroup.__doc__

    def __init__(self, *, nodes, name=None, **kwargs):
        super(SofistikNodesGroup, self).__init__(nodes=nodes, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

class SofistikPartsGroup(PartsGroup):
    """Sofistik implementation of :class:`compas_fea2.model.groups.PartsGroup`.\n
    """
    __doc__ += PartsGroup.__doc__

    def __init__(self, *, parts, name=None, **kwargs):
        super(SofistikPartsGroup, self).__init__(parts=parts, name=name, **kwargs)
        raise NotImplementedError

    def _generate_jobdata(self):
        raise NotImplementedError

