from itertools import combinations
from compas.geometry import is_point_on_plane, angle_planes
from compas.geometry import Plane


def nodes_on_plane(part, plane):
    """Find all the nodes of a part that belong to a given plane.

    Parameters
    ----------
    part : obj
        compas_fea2 :class:`PartBase` subclass
    plane : obl
        compas :class:`Plane`

    Return
    ------
    list
        list with the keys of the nodes belonging to the plane
    """
    return [node.key for node in part.nodes if is_point_on_plane(node.xyz, plane)]


# TODO implement all the Solid elements better than as it is done now...
def elements_on_plane(part, plane):
    """Find all the faces of the elements of a part that belong to a given plane.

    Warning
    -------
    It only works for tethrahedal elements

    Note
    ----
    The face labels are as follows:
        - S1: (0, 1, 2)
        - S2: (0, 1, 3)
        - S3: (1, 2, 3)
        - S4: (0, 2, 3)
    where the number is the index of the the node in the connectivity list

    Parameters
    ----------
    part : obj
        compas_fea2 :class:`PartBase` subclass
    plane : obl
        compas :class:`Plane`

    Returns
    -------
    dict
        element key, face
    """

    # find the nodes on the surfaces
    nodes_on_face = nodes_on_plane(part, plane)

    # find the elements on the surface
    surfaces_on_face = {}
    for element in part.elements.values():
        for c in element.connectivity:
            if c in nodes_on_face:
                if len(element.connectivity) == 4:
                    for combo in combinations(element.connectivity, 3):
                        points = [part.nodes[key].xyz for key in combo]
                        face = Plane.from_three_points(*points)
                        if angle_planes(plane, face, True) in [0, 180]:
                            face_names = {'s1': sorted([element.connectivity[i] for i in (0, 1, 2)]),
                                          's2': sorted([element.connectivity[i] for i in (0, 1, 3)]),
                                          's3': sorted([element.connectivity[i] for i in (1, 2, 3)]),
                                          's4': sorted([element.connectivity[i] for i in (0, 2, 3)])}
                            for k, v in face_names.items():
                                if sorted(list(combo)) == v:
                                    surfaces_on_face[element.key] = k
                            break
                elif len(element.connectivity) == 8:
                    for combo in combinations(element.connectivity, 4):
                        points = [part.nodes[key].xyz for key in combo]
                        face = Plane.from_three_points(*points[:-1])
                        if angle_planes(plane, face, True) in [0, 180]:
                            face_names = {'s1': sorted([element.connectivity[i] for i in (0, 1, 2, 3)]),
                                          's2': sorted([element.connectivity[i] for i in (4, 5, 6, 7)]),
                                          's3': sorted([element.connectivity[i] for i in (0, 1, 4, 5)]),
                                          's4': sorted([element.connectivity[i] for i in (1, 2, 5, 6)]),
                                          's5': sorted([element.connectivity[i] for i in (2, 3, 6, 7)]),
                                          's6': sorted([element.connectivity[i] for i in (0, 3, 4, 7)])}
                            for k, v in face_names.items():
                                if sorted(list(combo)) == v:
                                    surfaces_on_face[element.key] = k
                            break
                else:
                    raise TypeError(
                        f'Element {element.__repr__()} with {len(element.connectivity)} nodes is not supported')
    return surfaces_on_face
