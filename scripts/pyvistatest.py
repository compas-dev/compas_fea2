import pyvista as pv

# Create a sphere
sphere = pv.Sphere()

# Create a plotter and show the mesh
plotter = pv.Plotter()
plotter.add_mesh(sphere, color="blue")
plotter.show()