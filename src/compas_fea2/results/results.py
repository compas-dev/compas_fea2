from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
from compas.geometry import Frame
from compas.geometry import Transformation
from compas.geometry import Vector

from compas_fea2.base import FEAData
from compas_fea2.model import ElasticIsotropic


class Result(FEAData):
    """Result object defined at the nodes or elements. This ensures that the results from all
    the backends are consistently stored.

    Parameters
    ----------
    location : :class:`compas_fea2.model.Node` | :class:`compas_fea2.model._Element`
        The location of the result. It can be either a Node or an Element.
    components : dict
        A dictionary with {"component name": component value} for each component of the result.
    invariants : dict
        A dictionary with {"invariant name": invariant value} for each invariant of the result.

    Attributes
    ----------
    location : :class:`compas_fea2.model.Node` | :class:`compas_fea2.model._Element`
        The location of the result. I can be either a Node or an Element.
    components : dict
        A dictionary with {"component name": component value} for each component of the result.
    invariants : dict
        A dictionary with {"invariant name": invariant value} for each invariant of the result.

    """

    def __init__(self, location, **kwargs):
        super(Result, self).__init__(**kwargs)
        self._title = None
        self._registration = location
        self._components = {}
        self._invariants = {}

    @property
    def title(self):
        return self._title

    @property
    def location(self):
        return self._registration

    @property
    def reference_point(self):
        return self.location.reference_point

    @property
    def components(self):
        return self._components

    @property
    def invariants(self):
        return self._invariants

    def to_file(self, *args, **kwargs):
        raise NotImplementedError("this function is not available for the selected backend")

    def safety_factor(self, component, allowable):
        """Compute the safety factor (absolute ration value/limit) of the displacement.

        Parameters
        ----------
        component : int
            The component of the displacement vector. Either 1, 2, or 3.
        allowable : float
            Limit to compare with.

        Returns
        -------
        float
            The safety factor. Values higher than 1 are not safe.
        """
        return abs(self.vector[component] / allowable) if self.vector[component] != 0 else 1


class DisplacementResult(Result):
    """DisplacementResult object.

    Parameters
    ----------
    node : :class:`compas_fea2.model.Node`
        The location of the result.
    x : float
        The x component of the displacement vector
    y : float
        The y component of the displacement vector
    z : float
        The z component of the displacement vector

    Attributes
    ----------
    location : :class:`compas_fea2.model.Node` `
        The location of the result.
    node : :class:`compas_fea2.model.Node`
        The location of the result.
    components : dict
        A dictionary with {"component name": component value} for each component of the result.
    invariants : dict
        A dictionary with {"invariant name": invariant value} for each invariant of the result.
    u1 : float
        The x component of the displacement vector.
    u2 : float
        The y component of the displacement vector.
    u3 : float
        The z component of the displacement vector.
    vector : :class:`compas.geometry.Vector`
        The displacement vector.
    magnitude : float
        The absolute value of the displacement.

    Notes
    -----
    DisplacementResults are registered to a :class:`compas_fea2.model.Node`
    """

    def __init__(self, node, ux=0.0, uy=0.0, uz=0.0, uxx=0.0, uyy=0.0, uzz=0.0, **kwargs):
        super(DisplacementResult, self).__init__(location=node, **kwargs)
        self._title = "u"
        self._ux = ux
        self._uy = uy
        self._uz = uz
        self._uxx = uxx
        self._uyy = uyy
        self._uzz = uzz
        self._components = {"ux": ux, "uy": uy, "uz": uz, "uxx": uxx, "uyy": uyy, "uzz": uzz}
        self._vector = Vector(ux, uy, uz)
        self._vector_rotation = Vector(uxx, uyy, uzz)
        self._invariants = {"magnitude": self.vector.length}

    @property
    def node(self):
        return self._registration

    @property
    def ux(self):
        return self._ux

    @property
    def uy(self):
        return self._uy

    @property
    def uz(self):
        return self._uz

    @property
    def uxx(self):
        return self._uxx

    @property
    def uyy(self):
        return self._uyy

    @property
    def uzz(self):
        return self._uzz

    @property
    def vector(self):
        return self._vector

    @property
    def vector_rotation(self):
        return self._vector_rotation

    @property
    def magnitude(self):
        return self.vector.length


class ReactionResult(Result):
    """DisplacementResult object.

    Parameters
    ----------
    node : :class:`compas_fea2.model.Node`
        The location of the result.
    rf1 : float
        The x component of the reaction vector.
    rf2 : float
        The y component of the reaction vector.
    rf3 : float
        The z component of the reaction vector.

    Attributes
    ----------
    location : :class:`compas_fea2.model.Node` `
        The location of the result.
    node : :class:`compas_fea2.model.Node`
        The location of the result.
    components : dict
        A dictionary with {"component name": component value} for each component of the result.
    invariants : dict
        A dictionary with {"invariant name": invariant value} for each invariant of the result.
    rf1 : float
        The x component of the reaction vector.
    rf2 : float
        The y component of the reaction vector.
    rf3 : float
        The z component of the reaction vector.
    vector : :class:`compas.geometry.Vector`
        The displacement vector.
    magnitude : float
        The absolute value of the displacement.

    Notes
    -----
    ReactionResults are registered to a :class:`compas_fea2.model.Node`
    """

    def __init__(self, node, rfx, rfy, rfz, rfxx, rfyy, rfzz, **kwargs):
        super(ReactionResult, self).__init__(node, **kwargs)
        self._title = "rf"
        self._rfx = rfx
        self._rfy = rfy
        self._rfz = rfz
        self._rfxx = rfxx
        self._rfyy = rfyy
        self._rfzz = rfzz
        self._components = {"rfx": rfx, "rfy": rfy, "rfz": rfz, "rfxx": rfxx, "rfyy": rfyy, "rfzz": rfzz}
        self._vector = Vector(rfx, rfy, rfz)
        self._vector_moments = Vector(rfxx, rfyy, rfzz)
        self._invariants = {"magnitude": self.vector.length}

    @property
    def node(self):
        return self._registration

    @property
    def rfx(self):
        return self._rfx

    @property
    def rfy(self):
        return self._rfy

    @property
    def rfz(self):
        return self._rfz

    @property
    def rfxx(self):
        return self._rfxx

    @property
    def rfyy(self):
        return self._rfyy

    @property
    def rfzz(self):
        return self._rfzz

    @property
    def vector(self):
        return self._vector

    @property
    def magnitude(self):
        return self.vector.length


class SectionForcesResult(Result):
    """DisplacementResult object.

    Parameters
    ----------
    node : :class:`compas_fea2.model.Node`
        The location of the result.
    rf1 : float
        The x component of the reaction vector.
    rf2 : float
        The y component of the reaction vector.
    rf3 : float
        The z component of the reaction vector.

    Attributes
    ----------
    location : :class:`compas_fea2.model.Node` `
        The location of the result.
    node : :class:`compas_fea2.model.Node`
        The location of the result.
    components : dict
        A dictionary with {"component name": component value} for each component of the result.
    invariants : dict
        A dictionary with {"invariant name": invariant value} for each invariant of the result.
    rf1 : float
        The x component of the reaction vector.
    rf2 : float
        The y component of the reaction vector.
    rf3 : float
        The z component of the reaction vector.
    vector : :class:`compas.geometry.Vector`
        The displacement vector.
    magnitude : float
        The absolute value of the displacement.

    Notes
    -----
    SectionForcesResults are registered to a :class:`compas_fea2.model._Element
    """

    def __init__(self, node, **kwargs):
        super(SectionForcesResult, self).__init__(node, **kwargs)

    @property
    def forces_vector(self):
        pass

    @property
    def moments_vector(self):
        pass

    @property
    def element(self):
        return self.location


class StressResult(Result):
    """StressResult object.

    Parameters
    ----------
    element : :class:`compas_fea2.model._Element`
        The location of the result.
    s11 : float
        The 11 component of the stress tensor in local coordinates.
    s12 : float
        The 12 component of the stress tensor in local coordinates.
    s13 : float
        The 13 component of the stress tensor in local coordinates.
    s22 : float
        The 22 component of the stress tensor in local coordinates.
    s23 : float
        The 23 component of the stress tensor in local coordinates.
    s33 : float
        The 33 component of the stress tensor in local coordinates.


    Attributes
    ----------
    element : :class:`compas_fea2.model._Element`
        The location of the result.
    s11 : float
        The 11 component of the stress tensor in local coordinates.
    s12 : float
        The 12 component of the stress tensor in local coordinates.
    s13 : float
        The 13 component of the stress tensor in local coordinates.
    s22 : float
        The 22 component of the stress tensor in local coordinates.
    s23 : float
        The 23 component of the stress tensor in local coordinates.
    s33 : float
        The 33 component of the stress tensor in local coordinates.
    local_stress : numpy array
        The stress tensor in local coordinates.
    global_stress : numpy array
        The stress tensor in global coordinates.
    global_strains : numpy array
        The strsin tensor in global coordinates.
    I1 : numpy array
        First stress invariant.
    I2 : numpy array
        Second stress invariant.
    I3 : numpy array
        Second stress invariant.
    J2 : numpy array
        Second stress invariant of the deviatoric part.
    J3 : numpy array
        Second stress invariant of the deviatoric part.
    hydrostatic_stress : numpy array
        Hydrostatic stress.
    deviatoric_stress : numpy array
        Deviatoric stress.
    octahedral_stress : numpy array
        Octahedral normal and shear stresses
    principal_stresses_values : list(float)
        The eigenvalues sorted from low to high.
    principal_stresses_vectors : list(:class:`compas.geometry.Vector`)
        The eigenvectors sorted as according to the eigenvalues.
    principal_stresses : zip obj
        Iterator providing the eigenvalue/eigenvector pair.
    smin : float
        Minimum principal stress.
    smid : float
        Middle principal stress.
    smax : float
        Maximum principal stress.
    von_mises_stress : float
        Von Mises stress.

    Notes
    -----
    StressResults are registered to a :class:`compas_fea2.model._Element
    """

    def __init__(self, element, *, s11, s12, s13, s22, s23, s33, **kwargs):
        super(StressResult, self).__init__(element, **kwargs)
        self._title = None
        self._local_stress = np.array([[s11, s12, s13], [s12, s22, s23], [s13, s23, s33]])
        self._global_stress = self.transform_stress_tensor(self._local_stress, Frame.worldXY())
        self._components = {f"S{i+1}{j+1}": self._local_stress[i][j] for j in range(len(self._local_stress[0])) for i in range(len(self._local_stress))}

    @property
    def local_stress(self):
        # In local coordinates
        return self._local_stress

    @property
    def global_stress(self):
        # In global coordinates
        return self._global_stress

    @property
    def global_strain(self):
        if not isinstance(self.location.section.material, ElasticIsotropic):
            raise NotImplementedError("This function is currently only available for Elastic Isotropic materials")

        # For brevity
        s = self.global_stress
        v = self.element.section.material.v
        E = self.element.section.material.E

        dim = len(s)
        strain_tensor = np.zeros((dim, dim))

        # Calculate the strain tensor using Hooke's Law
        for i in range(dim):
            for j in range(dim):
                if i == j:  # Normal components
                    strain_tensor[i, j] = (s[i, j] - v * (self.I1 - s[i, j])) / E
                else:  # Shear components
                    strain_tensor[i, j] = (1 + v) * s[i, j] / E

        return strain_tensor

    @property
    def element(self):
        return self.location

    @property
    # First invariant
    def I1(self):
        return np.trace(self.global_stress)

    @property
    # Second invariant
    def I2(self):
        return 0.5 * (self.I1**2 - np.trace(np.dot(self.global_stress, self.global_stress)))

    @property
    # Third invariant
    def I3(self):
        return np.linalg.det(self.global_stress)

    @property
    # Second invariant of the deviatoric stress tensor: J2
    def J2(self):
        return 0.5 * np.trace(np.dot(self.deviatoric_stress, self.deviatoric_stress))

    @property
    # Third invariant of the deviatoric stress tensor: J3
    def J3(self):
        return np.linalg.det(self.deviatoric_stress)

    @property
    def hydrostatic_stress(self):
        return self.I1 / len(self.global_stress)

    @property
    def deviatoric_stress(self):
        return self.global_stress - np.eye(len(self.global_stress)) * self.hydrostatic_stress

    @property
    # Octahedral normal and shear stresses
    def octahedral_stresses(self):
        sigma_oct = self.I1 / 3
        tau_oct = np.sqrt(2 * self.J2 / 3)
        return sigma_oct, tau_oct

    @property
    def principal_stresses_values(self):
        eigenvalues = np.linalg.eigvalsh(self.global_stress)
        sorted_indices = np.argsort(eigenvalues)
        return eigenvalues[sorted_indices]

    @property
    def principal_stresses(self):
        return zip(self.principal_stresses_values, self.principal_stresses_vectors)

    @property
    def smax(self):
        return max(self.principal_stresses_values)

    @property
    def smin(self):
        return min(self.principal_stresses_values)

    @property
    def smid(self):
        if len(self.principal_stresses_values) == 3:
            return [x for x in self.principal_stresses_values if x != self.smin and x != self.smax]
        else:
            return None

    @property
    def principal_stresses_vectors(self):
        eigenvalues, eigenvectors = np.linalg.eig(self.global_stress)
        # Sort the eigenvalues/vectors from low to high
        sorted_indices = np.argsort(eigenvalues)
        eigenvectors = eigenvectors[:, sorted_indices]
        eigenvalues = eigenvalues[sorted_indices]
        return [Vector(*eigenvectors[:, i].tolist()) * abs(eigenvalues[i]) for i in range(len(eigenvalues))]

    @property
    def von_mises_stress(self):
        return np.sqrt(self.J2 * 3)

    @property
    def tresca_stress(self):
        return max(abs(self.principal_stresses_values - np.roll(self.principal_stresses_values, -1)))

    @property
    def safety_factor_max(self, allowable_stress):
        # Simple safety factor analysis based on maximum principal stress
        return abs(allowable_stress / self.smax) if self.smax != 0 else 1

    @property
    def safety_factor_min(self, allowable_stress):
        # Simple safety factor analysis based on maximum principal stress
        return abs(allowable_stress / self.smin) if self.smin != 0 else 1

    @property
    def strain_energy_density(self):
        """
        Calculates the strain energy density for linear elastic and isotropic materials.
        :return: The strain energy density value.
        """
        if not isinstance(self.location.section.material, ElasticIsotropic):
            raise NotImplementedError("Strain energy density calculation is currently only available for Elastic Isotropic materials")

        # Calculate strain energy density
        s = self.global_stress  # Stress tensor
        e = self.global_strain  # Strain tensor

        # For isotropic materials, using the formula: U = 1/2 * stress : strain
        U = 0.5 * np.tensile(s, e)

        return U

    def transform_stress_tensor(self, tensor, new_frame):
        """
        Transforms the stress tensor to a new frame using the provided 3x3 rotation matrix.
        This function works for both 2D and 3D stress tensors.

        Parameters:
        -----------
        new_frame : `class`:"compas.geometry.Frame"
            The new refernce Frame

        Returns:
        numpy array
            Transformed stress tensor as a numpy array of the same dimension as the input.
        """

        R = Transformation.from_change_of_basis(self.element.frame, new_frame)
        R_matrix = np.array(R.matrix)[:3, :3]

        return R_matrix @ tensor @ R_matrix.T

    def stress_along_direction(self, direction):
        """
        Computes the stress along a given direction.
        :param direction: A list or array representing the direction vector.
        :return: The normal stress along the given direction.
        """
        unit_direction = np.array(direction) / np.linalg.norm(direction)
        return unit_direction.T @ self.global_stress @ unit_direction

    def compute_mohr_circles_3d(self):
        """
        Computes the centers and radii of the three Mohr's circles for a 3D stress state.
        :return: A list of tuples, each containing the center and radius of a Mohr's circle.
        """
        # Ensure we're dealing with a 3D stress state
        if self.global_stress.shape != (3, 3):
            raise ValueError("Mohr's circles computation requires a 3D stress state.")

        # Calculate the centers and radii of the Mohr's circles
        circles = []
        for i in range(3):
            sigma1 = self.principal_stresses_values[i]
            for j in range(i + 1, 3):
                sigma2 = self.principal_stresses_values[j]
                center = (sigma1 + sigma2) / 2
                radius = abs(sigma1 - sigma2) / 2
                circles.append((center, radius))

        return circles

    def compute_mohr_circle_2d(self):
        # Ensure the stress tensor is 2D
        if self.global_stress.shape != (2, 2):
            raise ValueError("The stress tensor must be 2D for Mohr's Circle.")

        # Calculate the center and radius of the Mohr's Circle
        sigma_x, sigma_y, tau_xy = self.global_stress[0, 0], self.global_stress[1, 1], self.global_stress[0, 1]
        center = (sigma_x + sigma_y) / 2
        radius = np.sqrt(((sigma_x - sigma_y) / 2) ** 2 + tau_xy**2)

        # Create the circle
        theta = np.linspace(0, 2 * np.pi, 100)
        x = center + radius * np.cos(theta)
        y = radius * np.sin(theta)
        return x, y, center, radius, sigma_x, sigma_y, tau_xy

    def draw_mohr_circle_2d(self):
        """
        Draws the three Mohr's circles for a 3D stress state.
        """
        x, y, center, radius, sigma_x, sigma_y, tau_xy = self.compute_mohr_circle_2d()
        # Plotting
        plt.figure(figsize=(8, 8))
        plt.plot(x, y, label="Mohr's Circle")

        # Plotting the principal stresses
        plt.scatter([center + radius, center - radius], [0, 0], color="red")
        plt.text(center + radius, 0, "$\\sigma_1$")
        plt.text(center - radius, 0, "$\\sigma_2$")

        # Plotting the original stresses
        plt.scatter([sigma_x, sigma_y], [tau_xy, -tau_xy], color="blue")
        plt.text(sigma_x, tau_xy, "($\\sigma_x$, $\\tau$)")
        plt.text(sigma_y, -tau_xy, "($\\sigma_y$, $-\\tau$)")

        # Axes and grid
        plt.axhline(0, color="black", linewidth=0.5)
        plt.axvline(center, color="grey", linestyle="--", linewidth=0.5)
        plt.grid(color="gray", linestyle="--", linewidth=0.5)
        plt.xlabel("Normal Stress ($\\sigma$)")
        plt.ylabel("Shear Stress ($\\tau$)")
        plt.title("Mohr's Circle")
        plt.axis("equal")
        plt.legend()
        plt.show()

    def draw_mohr_circles_3d(self):
        """
        Draws the three Mohr's circles for a 3D stress state.
        """
        circles = self.compute_mohrs_circles_3d()

        # Create a figure and axis for the plot
        fig, ax = plt.subplots(figsize=(8, 8))

        # Plot each circle
        for i, (center, radius) in enumerate(circles, 1):
            circle = plt.Circle((center, 0), radius, fill=False, label=f"Circle {i}")
            ax.add_artist(circle)

            # Plot the center of the circle
            plt.scatter(center, 0, color="red")
            plt.text(center, 0, f"C{i}")

        # Set the limits and labels of the plot
        max_radius = max(radius for _, radius in circles)
        max_center = max(center for center, _ in circles)
        min_center = min(center for center, _ in circles)
        plt.xlim(min_center - max_radius - 10, max_center + max_radius + 10)
        plt.ylim(-max_radius - 10, max_radius + 10)
        plt.axhline(0, color="black", linewidth=0.5)
        plt.axvline(0, color="black", linewidth=0.5)
        plt.xlabel("Normal Stress ($\\sigma$)")
        plt.ylabel("Shear Stress ($\\tau$)")
        plt.title("Mohr's Circles for 3D Stress State")
        plt.legend()
        plt.grid(True)
        plt.axis("equal")

        # Show the plot
        plt.show()

    # =========================================================================
    #                               Yield Criteria
    # =========================================================================
    def mohr_coulomb(self, c, phi):
        return self.smax - self.smin - 2 * c * np.cos(phi) / (1 - np.sin(phi))

    # Drucker-Prager Criterion
    def drucker_prager(self, c, phi):
        # Convert angle from degrees to radians
        phi_radians = np.radians(phi)
        # Calculate material constants alpha and k from cohesion and internal friction angle
        alpha = np.sqrt(3) * (2 * np.sin(phi_radians)) / (3 - np.sin(phi_radians))
        k = np.sqrt(3) * c * (3 - np.sin(phi_radians)) / (3 * np.sin(phi_radians))
        return alpha * self.I1 + np.sqrt(self.J2) - k

    # Rankine Criterion
    def rankine(self, tensile_strength, compressive_strength):
        return max(self.smax - tensile_strength, abs(self.smin) - compressive_strength)

    # Bresler-Pister Criterion (simplified version)
    def bresler_pister(self, tensile_strength, compressive_strength):
        return max(self.smax / tensile_strength, abs(self.smin) / compressive_strength)

    # Modified Mohr Criterion (simplified version)
    def modified_mohr(self, tensile_strength):
        return (self.smax - self.smin) / 2 - tensile_strength

    # Griffith Criterion
    def griffith(self, fracture_toughness):
        return self.smax**2 / (2 * fracture_toughness)

    # Lade-Duncan Criterion (simplified version)
    def lade_duncan(self, c):
        return self.I1 - 3 * c

    def thermal_stress_analysis(self, temperature_change):
        # Simple thermal stress analysis for isotropic material
        if not isinstance(self.location.section.material, ElasticIsotropic):
            raise NotImplementedError("This function is only available for Elastic Isotropic materials")
        # Delta_sigma = E * alpha * Delta_T
        return self.location.section.material.E * self.location.section.material.expansion * temperature_change


class SolidStressResult(StressResult):
    def __init__(self, element, *, s11, s12, s13, s22, s23, s33, **kwargs):
        super(SolidStressResult, self).__init__(element=element, s11=s11, s12=s12, s13=s13, s22=s22, s23=s23, s33=s33, **kwargs)
        self._title = "s3d"


class MembraneStressResult(StressResult):
    def __init__(self, element, *, s11, s12, s22, **kwargs):
        super(MembraneStressResult, self).__init__(element, s11=s11, s12=s12, s13=0, s22=s22, s23=0, s33=0, **kwargs)
        self._title = "s2d"


class ShellStressResult(MembraneStressResult):
    def __init__(self, element, *, s11, s12, s22, m11, m22, m12, **kwargs):
        super(ShellStressResult, self).__init__(element, s11=s11, s12=s12, s22=s22, **kwargs)
        self._title = "s2d"
        self._local_bending_moments = np.array([[m11, m12, 0], [m12, m22, 0], [0, 0, 0]])
        self._local_stress_top = self.local_stress_membrane + 6 / self.element.section.t**2 * self._local_bending_moments
        self._local_stress_bottom = self.local_stress_membrane - 6 / self.element.section.t**2 * self._local_bending_moments

        # self._global_stress_membrane = self.transform_stress_tensor(self.local_stress_membrane, Frame.worldXY())
        self._global_stress_top = self.transform_stress_tensor(self.local_stress_top, Frame.worldXY())
        self._global_stress_bottom = self.transform_stress_tensor(self.local_stress_bottom, Frame.worldXY())

        self._stress_components = {f"S{i+1}{j+1}": self._local_stress[i][j] for j in range(len(self._local_stress[0])) for i in range(len(self._local_stress))}
        self._bending_components = {
            f"M{i+1}{j+1}": self._local_bending_moments[i][j] for j in range(len(self._local_bending_moments[0])) for i in range(len(self._local_bending_moments))
        }

    @property
    def local_stress_membrane(self):
        return self._local_stress

    @property
    def local_stress_bottom(self):
        return self._local_stress_bottom

    @property
    def local_stress_top(self):
        return self._local_stress_top

    @property
    def global_stress_membrane(self):
        return self._global_stress  # self._global_stress_membrane

    @property
    def global_stress_top(self):
        return self._global_stress_top

    @property
    def global_stress_bottom(self):
        return self._global_stress_bottom

    @property
    def hydrostatic_stress_top(self):
        return self.I1_top / len(self.global_stress_top)

    @property
    def hydrostatic_stress_bottom(self):
        return self.I1_bottom / len(self.global_stress_bottom)

    @property
    def deviatoric_stress_top(self):
        return self.global_stress_top - np.eye(len(self.global_stress_top)) * self.hydrostatic_stress_top

    @property
    def deviatoric_stress_bottom(self):
        return self.global_stress_bottom - np.eye(len(self.global_stress_bottom)) * self.hydrostatic_stress_bottom

    @property
    # First invariant
    def I1_top(self):
        return np.trace(self.global_stress_top)

    @property
    # First invariant
    def I1_bottom(self):
        return np.trace(self.global_stress_bottom)

    @property
    # Second invariant
    def I2_top(self):
        return 0.5 * (self.I1_top**2 - np.trace(np.dot(self.global_stress_top, self.global_stress_top)))

    @property
    # Second invariant
    def I2_bottom(self):
        return 0.5 * (self.I2_bottom**2 - np.trace(np.dot(self.global_stress_bottom, self.global_stress_bottom)))

    @property
    # Third invariant
    def I3_top(self):
        return np.linalg.det(self.global_stress_top)

    @property
    # Third invariant
    def I3_bottom(self):
        return np.linalg.det(self.global_stress_bottom)

    @property
    # Second invariant of the deviatoric stress tensor: J2
    def J2_top(self):
        return 0.5 * np.trace(np.dot(self.deviatoric_stress_top, self.deviatoric_stress_top))

    @property
    # Second invariant of the deviatoric stress tensor: J2
    def J2_bottom(self):
        return 0.5 * np.trace(np.dot(self.deviatoric_stress_bottom, self.deviatoric_stress_bottom))

    @property
    # Third invariant of the deviatoric stress tensor: J3
    def J3_top(self):
        return np.linalg.det(self.deviatoric_stress_top)

    @property
    # Third invariant of the deviatoric stress tensor: J3
    def J3_bottom(self):
        return np.linalg.det(self.deviatoric_stress_bottom)

    @property
    def principal_stresses_values(self):
        eigenvalues = np.linalg.eigvalsh(self.global_stress[:2, :2])
        sorted_indices = np.argsort(eigenvalues)
        return eigenvalues[sorted_indices]

    @property
    def principal_stresses_values_top(self):
        eigenvalues = np.linalg.eigvalsh(self.global_stress_top[:2, :2])
        sorted_indices = np.argsort(eigenvalues)
        return eigenvalues[sorted_indices]

    @property
    def principal_stresses_values_bottom(self):
        eigenvalues = np.linalg.eigvalsh(self.global_stress_bottom[:2, :2])
        sorted_indices = np.argsort(eigenvalues)
        return eigenvalues[sorted_indices]

    @property
    def principal_stresses_vectors(self):
        eigenvalues, eigenvectors = np.linalg.eig(self.global_stress[:2, :2])
        # Sort the eigenvalues/vectors from low to high
        sorted_indices = np.argsort(eigenvalues)
        eigenvectors = eigenvectors[:, sorted_indices]
        eigenvalues = eigenvalues[sorted_indices]
        return [Vector(*eigenvectors[:, i].tolist()) * abs(eigenvalues[i]) for i in range(len(eigenvalues))]

    @property
    def principal_stresses_vectors_top(self):
        eigenvalues, eigenvectors = np.linalg.eig(self.global_stress_top[:2, :2])
        # Sort the eigenvalues/vectors from low to high
        sorted_indices = np.argsort(eigenvalues)
        eigenvectors = eigenvectors[:, sorted_indices]
        eigenvalues = eigenvalues[sorted_indices]
        return [Vector(*eigenvectors[:, i].tolist()) * abs(eigenvalues[i]) for i in range(len(eigenvalues))]

    @property
    def principal_stresses_vectors_bottom(self):
        eigenvalues, eigenvectors = np.linalg.eig(self.global_stress_bottom[:2, :2])
        # Sort the eigenvalues/vectors from low to high
        sorted_indices = np.argsort(eigenvalues)
        eigenvectors = eigenvectors[:, sorted_indices]
        eigenvalues = eigenvalues[sorted_indices]
        return [Vector(*eigenvectors[:, i].tolist()) * abs(eigenvalues[i]) for i in range(len(eigenvalues))]

    @property
    def principal_stresses_top(self):
        return zip(self.principal_stresses_values_top, self.principal_stresses_vectors_top)

    @property
    def principal_stresses_bottom(self):
        return zip(self.principal_stresses_values_bottom, self.principal_stresses_vectors_bottom)

    @property
    def von_mises_stress_top(self):
        return np.sqrt(self.J2_top * 3)

    @classmethod
    def from_components(cls, location, components):
        stress_components = {k.lower(): v for k, v in components.items() if k in ("S11", "S22", "S12")}
        bending_components = {k.lower(): v for k, v in components.items() if k in ("M11", "M22", "M12")}
        return cls(location, **stress_components, **bending_components)

    def membrane_stress(self, frame):
        return self.transform_stress_tensor(self.local_stress_membrane, frame)

    def top_stress(self, frame):
        return self.transform_stress_tensor(self.local_stress_top, frame)

    def bottom_stress(self, frame):
        return self.transform_stress_tensor(self.local_stress_bottom, frame)

    def stress_along_direction(self, direction, side="mid"):
        tensors = {"mid": self.global_stress_bottom, "top": self.global_stress_top, "bottom": self.global_stress_bottom}
        unit_direction = np.array(direction) / np.linalg.norm(direction)
        return unit_direction.T @ tensors[side] @ unit_direction
