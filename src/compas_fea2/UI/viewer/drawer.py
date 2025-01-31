from compas.colors import Color
from compas.colors import ColorMap
from compas.geometry import Line


def draw_field_vectors(locations, vectors, scale_results, translate=0, high=None, low=None, cmap=None, **kwargs):
    """Display a given vector field.

    Parameters
    ----------
    field_locations : list
        The locations of the field.
    field_results : list
        The results of the field.
    scale_results : float
        The scale factor for the results.
    translate : float
        The translation factor for the results.
    """
    colors = []
    lines = []
    if cmap:
        lengths = [v.length for v in vectors]
        min_value = high or min(lengths)
        max_value = low or max(lengths)
    else:
        colors = [Color.red()] * len(vectors)

    for pt, vector in zip(list(locations), list(vectors)):
        if vector.length == 0:
            continue
        else:
            v = vector.scaled(scale_results)
            lines.append(Line.from_point_and_vector(pt, v).translated(v * translate))
            if cmap:
                colors.append(cmap(vector.length, minval=min_value, maxval=max_value))
    return lines, colors


def draw_field_contour(model, field_locations, field_results, high=None, low=None, cmap=None, **kwargs):
    """Display a given scalar field.

    Parameters
    ----------
    field_locations : list
        The locations of the field.
    field_results : list
        The results of the field.
    high : float
        The maximum value of the field.
    low : float
        The minimum value of the field.
    cmap : :class:`compas.colors.ColorMap`
        The color map for the field.
    """
    # # Get values
    min_value = high or min(field_results)
    max_value = low or max(field_results)
    cmap = cmap or ColorMap.from_palette("hawaii")

    # Get mesh
    part_vertexcolor = {}
    for part in model.parts:
        if not part.discretized_boundary_mesh:
            continue
        # Color the mesh
        vertexcolor = {}
        gkey_vertex = part.discretized_boundary_mesh.gkey_vertex(3)
        for n, v in zip(field_locations, field_results):
            if not n.part == part:
                continue
            if kwargs.get("bound", None):
                if v >= kwargs["bound"][1] or v <= kwargs["bound"][0]:
                    color = Color.red()
                else:
                    color = cmap(v, minval=min_value, maxval=max_value)
            else:
                color = cmap(v, minval=min_value, maxval=max_value)
                vertex = gkey_vertex.get(n.gkey, None)
                vertexcolor[vertex] = color
        part_vertexcolor[part] = vertexcolor

    return part_vertexcolor
