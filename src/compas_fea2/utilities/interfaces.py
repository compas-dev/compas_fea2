
from compas_fea2.model.elements import SolidElement

from compas.geometry import is_point_in_polygon_xy
from compas.geometry import is_point_on_plane, angle_planes
from compas.geometry import Plane
from compas.geometry import Frame
from compas.geometry import Transformation
from compas.geometry import Point


def nodes_on_plane(part, plane):
    """Find all the nodes of a part that belong to a given plane.

    Parameters
    ----------
    part : :class:`compas_fea2.model.Part`
        Part to check
    plane : :class:`compas_fea2.model.Interface`
        Plane where to find the nodes

    Return
    ------
    list
        list with the nodes of the part belonging to the plane
    """
    return [node for node in part.nodes if is_point_on_plane(node.xyz, plane)]


def nodes_in_interface(part, interface, mark=False):
    """Find all the nodes of a part beloging to an interface.

    Parameters
    ----------
    part : :class:`compas_fea2.model.Part`
        The part.
    interface : :class:`compas_fea2.model.interface`
        The interface.
    mark : bool, optional
        If `True` mark set ``node.on_interface = True``, by default `False`.

    Returns
    -------
    list
        List with the nodes.
    """
    T = Transformation.from_frame_to_frame(interface.frame, Frame.worldXY())

    nodes = []
    for node in nodes_on_plane(part, Plane.from_frame(interface.frame)):
        interface_xy = [Point(*point) for point in interface.points]
        for point in interface_xy:
            point.transform(T)
        nodes_xy = Point(*node.xyz)
        nodes_xy.transform(T)
        if is_point_in_polygon_xy(nodes_xy, interface_xy):
            nodes.append(node)
            if mark:
                node.on_interface = True
    return nodes


def faces_on_plane(part, plane):
    """Find the face of the elements of a part that belongs to a given plane, if any.

    Note
    ----
    The search is limited to solid elements.

    Parameters
    ----------
    part : :class:`compas_fea2.model.Part`
        The part to search.
    plane : :class:`compas.geometry.Plane`
        The plane where the faces should belong.

    Returns
    -------
    dict
        element, face name
    """

    faces = []
    for element in filter(lambda x: isinstance(x, SolidElement), part.elements):
        for face in element.faces:
            if angle_planes(plane, face.plane, True) in [0, 180] and is_point_on_plane(face.plane.point, plane):
                faces.append(face)
    return faces


def faces_in_interface(part, interface, extend=False, mark=False):
    """Return the face of the elements of a given part laying of a given interface.

    Parameters
    ----------
    part : :class:`compsa_fea2.model.Part`
        The part of the model to check.
    interface : :class:`compas_fea2.model.interface`
        The interface where the faces must lay.
    extend : bool, optional
        If ``True``, include also those faces that are only partially contained
        within the interface (at least one node inside the interface). By default
        ``False``.
    mark : bool, optional
        If `True` mark set ``node.on_interface = True``, by default `False`.

    Returns
    -------
    :class:list[`compas_fea2.model.elements.Face`]
        list of the faces on the interface.
    """
    func = any if extend else all
    return [face for face in faces_on_plane(part, Plane.from_frame(interface.frame)) if func(node in nodes_in_interface(part, interface, mark=mark) for node in face.nodes)]
