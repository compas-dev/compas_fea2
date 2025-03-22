import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from compas.geometry import Polygon, Point

# Define the polygon as a Shapely object
polygon_coords = [
    [0, 0], [5, 0], [6, 3], [3, 5], [0, 3], [0, 0]  # Closing the polygon
]
polygon = Polygon(polygon_coords)

# Generate random points inside the polygon
num_points = 20

points = []

while len(points) < num_points:
    x, y = np.random.uniform(min_x, max_x), np.random.uniform(min_y, max_y)
    if polygon.contains(Point(x, y)):
        points.append([x, y])

points = np.array(points)

# Add polygon vertices to ensure boundary fidelity
points = np.vstack((points, polygon_coords[:-1]))  # Exclude duplicate last point

# Perform Delaunay triangulation
tri = Delaunay(points)

# Filter triangles to keep only those inside the polygon
valid_triangles = []
for simplex in tri.simplices:
    # Get the triangle vertices
    triangle = Polygon(points[simplex])
    
    # Check if the triangle is fully inside the polygon
    if polygon.contains(triangle):
        valid_triangles.append(simplex)

# Plot results
plt.figure(figsize=(8, 6))
plt.plot(*polygon.exterior.xy, 'k-', linewidth=2, label="Polygon Boundary")

# Plot valid Delaunay triangles
for simplex in valid_triangles:
    triangle = points[simplex]
    plt.fill(triangle[:, 0], triangle[:, 1], edgecolor='black', fill=False)

# Plot points
plt.scatter(points[:, 0], points[:, 1], color='red', zorder=3, label="Points")

plt.legend()
plt.title("Delaunay Triangulation Inside a Polygon")
plt.show()