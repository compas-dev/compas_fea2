from compas.geometry import Plane
from compas.geometry import Brep

from compas_view2.app import Controller
from compas_view2.objects import Collection


class FEA2Controller(Controller):
    def placeholder(self, *args, **kwargs):
        pass

    # =============================================================================
    # Sidebar
    # =============================================================================

    def toggle_horizontal_section(self, *args, **kwargs):
        state = args[0]

        self.app._controls["vertical_section_checkbox"].set_checked_state(False)
        self.app._controls["horizontal_section_checkbox"].set_checked_state(state)

        for obj in self.app.view.objects:
            obj.is_visible = not state

        self.app.horizontal_slices.is_visible = state
        self.app.vertical_slices.is_visible = False
        self.app.view.update()

    def toggle_vertical_section(self, *args, **kwargs):
        state = args[0]

        self.app._controls["horizontal_section_checkbox"].set_checked_state(False)
        self.app._controls["vertical_section_checkbox"].set_checked_state(state)

        for obj in self.app.view.objects:
            obj.is_visible = not state

        self.app.horizontal_slices.is_visible = False
        self.app.vertical_slices.is_visible = state
        self.app.view.update()

    # =============================================================================
    # Geometry
    # =============================================================================

    def load_step(self, *args, **kwargs):
        pass

    def load_obj(self, *args, **kwargs):
        pass

    def set_horizontal_section(self, *args, **kwargs):
        slicer = Plane((0, 0, 400), (0, 0, 1))
        toslice = [obj for obj in self.app.view.objects if isinstance(obj._data, Brep)]
        slices = []
        # combine the objects into 1 compound brep
        for obj in toslice:
            brep = obj._data
            slice = brep.slice(slicer)
            slices.append(slice)
        self.app.remove(self.app.horizontal_slices)
        obj = self.app.add(Collection(slices))
        self.app.horizontal_slices = obj
        self.toggle_horizontal_section(True)

    def set_vertical_section(self, *args, **kwargs):
        slicer = Plane((0, 2500, 0), (0, 1, 0))
        toslice = [obj for obj in self.app.view.objects if isinstance(obj._data, Brep)]
        slices = []
        # combine the objects into 1 compound brep
        for obj in toslice:
            brep = obj._data
            slice = brep.slice(slicer)
            slices.append(slice)
        self.app.remove(self.app.vertical_slices)
        obj = self.app.add(Collection(slices))
        self.app.vertical_slices = obj
        self.toggle_vertical_section(True)

    def gaussian_curvature(self, *args, **kwargs):
        pass

    # =============================================================================
    # Assembly
    # =============================================================================

    def identify_interfaces(self, *args, **kwargs):
        pass

    # =============================================================================
    # DEM
    # =============================================================================

    # =============================================================================
    # FEA
    # =============================================================================
