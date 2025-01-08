from compas.colors import Color
from compas.colors import ColorMap
from compas.geometry import Line


def draw_field_vectors(field_locations, field_vectors, scale_results, translate=0, high=None, low=None, cmap=None, **kwargs):
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
    vectors = []
    colors = []
    
    if cmap:
        lengths = [v.length for v in field_vectors]
        min_value = high or min(lengths)
        max_value = low or max(lengths)
    else:
        colors = [Color.red()]* len(field_vectors)

    for pt, vector in zip(list(field_locations), list(field_vectors)):
        if vector.length == 0:
            continue
        else:
            v = vector.scaled(scale_results)
            vectors.append(Line.from_point_and_vector(pt, v).translated(v * translate))
            if cmap:
                colors.append(cmap(vector.length, minval=min_value, maxval=max_value))
    return vectors, colors


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


def draw_reactions(self, step=None, scale_results=1, translate=0, components=None):
    """Display the reaction forces.

    Parameters
    ----------
    step : str
        The step to display the reactions from.
    scale_results : float
        The scale factor for the results.
    translate : float
        The translation factor for the results.
    components : list
        The components to display.
    """
    from compas_viewer.scene import Collection

    if not step:
        step = self.steps_order[-1]
    field_locations = list(self.reaction_field.locations(step, point=True))
    field_results = list(self.reaction_field.vectors(step))

    if not components:
        components = [0, 1, 2]

    collections = []
    for component in components:
        lines = self.draw_field_vectors(field_locations, field_results, scale_results, translate=translate)
        collections.append((Collection(lines), {"name": f"RF-{component}", "linecolor": Color.green(), "linewidth": 3}))
    return collections
