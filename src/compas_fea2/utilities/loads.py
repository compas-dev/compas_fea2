def mesh_points_pattern(model, mesh, t=0.05, side='top'):
    """Find all the nodes of a model vertically (z) aligned with the vertices of a given mesh.

    Parameters
    ----------
    model : :class:`compas_fea2.model.Model`
        The model
    mesh : :class:`compas.datastructures.Mesh`
        The mesh
    t : float, optional
        A prescribed tolerance for the search, by default 0.05
    side : str, optional
        filter the nodes to one side, by default 'top'

    Returns
    -------
    dict
        {vertex:{'area': float,
                'nodes':[:class:`compas_fea2.model.Node`]},
                }
    """

    pattern = {}
    for vertex in mesh.vertices():
        point = mesh.vertex_coordinates(vertex)
        tributary_area = mesh.vertex_area(vertex)
        for part in model.parts: #filter(lambda p: 'block' in p.name, model.parts):
            nodes = part.find_nodes_where(
                [f'{point[0]-t} <= x <= {point[0]+t}', f'{point[1]-t} <= y <= {point[1]+t}'])
            if nodes:
                if side == 'top':
                    pattern.setdefault(vertex, {})['area'] = tributary_area
                    pattern[vertex].setdefault('nodes', []).append(list(sorted(nodes, key=lambda n: n.z))[-1])
                # TODO add additional sides
    return pattern
