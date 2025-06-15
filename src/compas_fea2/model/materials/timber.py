from .material import _Material


class Timber(_Material):
    """Base class for Timber material"""

    def __init__(self, *, density, **kwargs):
        """
        Parameters
        ----------
        density : float
            Density of the timber material [kg/m^3].
        name : str, optional
            Name of the material.
        """
        super().__init__(density=density, **kwargs)

    @property
    def __data__(self):
        return {
            "density": self.density,
            "name": self.name,
        }

    @classmethod
    def __from_data__(cls, data):
        return cls(
            density=data["density"],
            name=data["name"],
        )
