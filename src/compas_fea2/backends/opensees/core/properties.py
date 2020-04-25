
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fea2._core import cElementProperties

# Author(s): Andrew Liew (github.com/andrewliew), Tomas Mendez Echenagucia (github.com/tmsmendez)


__all__ = [
    'ElementProperties'
]


class ElementProperties(cElementProperties):

    """ Initialises an ElementProperties object.

    Parameters
    ----------
    name : str
        Key name for the ElementProperties object.
    material : str
        Name of the Material object to assign.
    section : str
        Name of the Section object to assign.
    elements : list
        Element keys assignment.

    Attributes
    ----------
    name : str
        Key name for the ElementProperties object.
    material : str
        Name of the Material object to assign.
    section : str
        Name of the Section object to assign.
    elements : list
        Element keys assignment.


    """
    pass
    # def __init__(self, name, material, section, elset, elements, rebar):
    #     super(ElementProperties, self).__init__(name, material, section, elset, elements, rebar)
