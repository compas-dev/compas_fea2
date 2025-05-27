import numpy as np
from compas.itertools import remap_values
from compas.scene import register
from compas.scene import register_scene_objects
from compas_viewer.components import Button
from compas_viewer.scene import GroupObject
from compas_viewer.viewer import Viewer

from compas_fea2.UI.viewer.scene import FEA2ModelObject
from compas_fea2.UI.viewer.scene import FEA2NodeFieldResultsObject
from compas_fea2.UI.viewer.scene import FEA2StepObject
from compas_fea2.UI.viewer.scene import FEA2Stress2DFieldResultsObject


def toggle_nodes():
    viewer = FEA2Viewer()
    if viewer.nodes:
        for obj in viewer.nodes.descendants:
            obj.is_visible = not obj.is_visible
    viewer.renderer.update()


def toggle_supports():
    viewer = FEA2Viewer()
    if viewer.supports:
        for obj in viewer.supports.descendants:
            obj.is_visible = not obj.is_visible
    viewer.renderer.update()


def toggle_blocks():
    viewer = FEA2Viewer()
    if viewer.blocks:
        for obj in viewer.blocks.descendants:
            obj.is_visible = not obj.is_visible
    viewer.renderer.update()


def toggle_blockfaces():
    viewer = FEA2Viewer()
    if viewer.blocks:
        for obj in viewer.blocks.descendants:
            obj.show_faces = not obj.show_faces
    viewer.renderer.update()


def toggle_interfaces():
    viewer = FEA2Viewer()
    if viewer.interfaces:
        for obj in viewer.interfaces.descendants:
            obj.is_visible = not obj.is_visible
    viewer.renderer.update()


def toggle_compression():
    viewer = FEA2Viewer()
    if viewer.compressionforces:
        for obj in viewer.compressionforces.descendants:
            obj.is_visible = not obj.is_visible
    viewer.renderer.update()


def toggle_tension():
    viewer = FEA2Viewer()
    if viewer.tensionforces:
        for obj in viewer.tensionforces.descendants:
            obj.is_visible = not obj.is_visible
    viewer.renderer.update()


def toggle_friction():
    viewer = FEA2Viewer()
    if viewer.frictionforces:
        for obj in viewer.frictionforces.descendants:
            obj.is_visible = not obj.is_visible
    viewer.renderer.update()


def toggle_resultants():
    viewer = FEA2Viewer()
    if viewer.resultantforces:
        for obj in viewer.resultantforces.descendants:
            obj.is_visible = not obj.is_visible
    viewer.renderer.update()


def scale_compression(value):
    if value <= 50:
        values = list(range(1, 51))
        values = remap_values(values, target_min=1, target_max=100)
        scale = values[value - 1] / 100
    else:
        value = value - 50
        values = list(range(0, 50))
        values = remap_values(values, target_min=1, target_max=100)
        scale = values[value - 1]

    viewer = FEA2Viewer()
    if viewer.compressionforces:
        for obj, line in zip(viewer.compressionforces.descendants, viewer._compressionforces):
            obj.geometry.start = line.midpoint - line.vector * 0.5 * scale
            obj.geometry.end = line.midpoint + line.vector * 0.5 * scale
            obj.update()
    viewer.renderer.update()


class FEA2Viewer(Viewer):
    """Viewer for FEA2 models.

    Parameters
    ----------
    model : :class:`compas_fea2.model.Structure`
        The FEA2 model to visualize.
    scale_model : float
        The scale factor for the model.
    """

    def __init__(self, center=[1, 1, 1], scale_model=1000, **kwargs):
        super().__init__(**kwargs)
        self.renderer.camera.target = [i * scale_model for i in center]
        self.config.vectorsize = 0.2
        V1 = np.array([0, 0, 0])
        V2 = np.array(self.renderer.camera.target)
        delta = V2 - V1
        length = np.linalg.norm(delta)
        distance = length * 3
        unitSlope = delta / length
        new_position = V1 + unitSlope * distance
        self.renderer.camera.position = new_position.tolist()
        self.renderer.camera.near *= 1
        self.renderer.camera.far *= 10000
        self.renderer.camera.scale *= scale_model

        self.model: GroupObject = None
        self.nodes: GroupObject = None
        self.displacements: GroupObject = None
        self.reactions: GroupObject = None
        self.step: GroupObject = None

        self.ui.sidedock.show = True
        self.ui.sidedock.add(Button(text="Toggle Nodes", action=toggle_nodes))
        self.ui.sidedock.add(Button(text="Toggle Supports", action=toggle_supports))
        self.ui.sidedock.add(Button(text="Toggle Blocks", action=toggle_blocks))
        self.ui.sidedock.add(Button(text="Toggle Block Faces", action=toggle_blockfaces))
        self.ui.sidedock.add(Button(text="Toggle Interfaces", action=toggle_interfaces))
        self.ui.sidedock.add(Button(text="Toggle Compression", action=toggle_compression))
        self.ui.sidedock.add(Button(text="Toggle Tension", action=toggle_tension))
        self.ui.sidedock.add(Button(text="Toggle Friction", action=toggle_friction))
        self.ui.sidedock.add(Button(text="Toggle Resultants", action=toggle_resultants))
        register_scene_objects()

    def add_parts(self, parts):
        pass

    def add_model(self, model, fast=True, show_parts=True, opacity=0.5, show_bcs=True, show_loads=True, **kwargs):
        register_scene_objects()
        register(model.__class__.__base__, FEA2ModelObject, context="Viewer")
        self.model = self.scene.add(model, fast=fast, show_parts=show_parts, opacity=opacity, show_bcs=show_bcs, show_loads=show_loads, **kwargs)

    def add_displacement_field(
        self, field, component=None, fast=False, show_parts=True, opacity=0.5, show_bcs=True, show_loads=True, show_vectors=True, show_contours=False, **kwargs
    ):
        register(field.__class__.__base__, FEA2NodeFieldResultsObject, context="Viewer")
        self.displacements = self.scene.add(
            item=field,
            component=component,
            fast=fast,
            show_parts=show_parts,
            opacity=opacity,
            show_bcs=show_bcs,
            show_loads=show_loads,
            show_vectors=show_vectors,
            show_contours=show_contours,
            **kwargs,
        )

    def add_reaction_field(
        self, field, model, component=None, fast=False, show_parts=True, opacity=0.5, show_bcs=True, show_loads=True, show_vectors=True, show_contours=False, **kwargs
    ):
        register(field.__class__.__base__, FEA2NodeFieldResultsObject, context="Viewer")
        self.reactions = self.scene.add(
            field,
            model=model,
            component=component,
            fast=fast,
            show_parts=show_parts,
            opacity=opacity,
            show_bcs=show_bcs,
            show_loads=show_loads,
            show_vectors=show_vectors,
            show_contours=show_contours,
            **kwargs,
        )

    def add_stress2D_field(
        self, field, model, component=None, fast=False, show_parts=True, opacity=0.5, show_bcs=True, show_loads=True, show_vectors=1, show_contours=False, plane="mid", **kwargs
    ):
        register(field.__class__.__base__, FEA2Stress2DFieldResultsObject, context="Viewer")
        self.stresses = self.scene.add(
            field,
            model=model,
            component=component,
            fast=fast,
            show_parts=show_parts,
            opacity=opacity,
            show_bcs=show_bcs,
            show_loads=show_loads,
            show_vectors=show_vectors,
            show_contours=show_contours,
            plane=plane,
            **kwargs,
        )

    def add_mode_shape(self, mode_shape, component=None, fast=False, show_parts=True, opacity=0.5, show_bcs=True, show_loads=True, **kwargs):
        register(mode_shape.__class__.__base__, FEA2NodeFieldResultsObject, context="Viewer")
        self.displacements = self.scene.add(mode_shape, component=component, fast=fast, show_parts=show_parts, opacity=opacity, show_bcs=show_bcs, show_loads=show_loads, **kwargs)

    def add_step(self, step, show_loads=1):
        register(step.__class__, FEA2StepObject, context="Viewer")
        self.step = self.scene.add(step, step=step, scale_factor=show_loads)

    def add_nodes(self, nodes):
        self.nodes = []
        for node in nodes:
            self.nodes.append(
                (
                    node.point,
                    {
                        # "pointcolor": Color.grey(),
                        "pointßsize": 10,
                        "opacity": 0.5,
                        "name": node.name,
                    },
                )
            )

        self.scene.add(
            self.nodes,
            name="Nodes",
        )
