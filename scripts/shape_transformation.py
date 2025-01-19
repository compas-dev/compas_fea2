from compas_fea2.model.shapes import Rectangle, Frame

r = Rectangle(w=100, h=300)
print(r.summary())

# Example of applying a transformation:
new_frame = Frame([0, 0, 1000], [1, 0, 0], [0, 1, 0])
r_transf = r.oriented(new_frame)

# Convert to meshes (if needed):
m1 = r.to_mesh()
m2 = r_transf.to_mesh()

print(m1)

print("Original rectangle centroid:", r.centroid)
print("Transformed rectangle centroid:", r_transf.centroid)
