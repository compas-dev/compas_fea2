import numpy as np
from shapely.geometry import Polygon
from scipy.spatial import KDTree
from numpy.linalg import solve
from compas.geometry import Frame, centroid_points, cross_vectors, local_to_world_coordinates_numpy
from compas_fea2.model.interfaces import Interface


def mesh_mesh_interfaces(a, b, tmax=1e-6, amin=1e-1):
    """Optimized face-face contact detection between two meshes."""

    # -------------------------------------------------------------------------
    # 1. Precompute data for B
    # -------------------------------------------------------------------------
    # (a) Store B's vertices once as a NumPy array
    b_xyz = np.array(b.vertices_attributes("xyz"), dtype=float).T
    # (b) Map each vertex key to index
    k_i = {key: index for index, key in enumerate(b.vertices())}
    # (c) Precompute face centers for B (used in KDTree)
    face_centers_b = np.array([b.face_center(f) for f in b.faces()])
    # (d) Build a KDTree from B’s face centers
    if len(face_centers_b) == 0:
        print("No faces in mesh B. Exiting.")
        return []
    tree = KDTree(face_centers_b)
    # (e) Precompute face-to-vertex indices so we don’t call b.face_vertices(f1) repeatedly
    b_face_vertex_indices = []
    for f1 in b.faces():
        vertex_keys = b.face_vertices(f1)
        b_face_vertex_indices.append([k_i[vk] for vk in vertex_keys])

    # -------------------------------------------------------------------------
    # 2. Precompute frames for each face in A
    # -------------------------------------------------------------------------
    frames = {}
    for face in a.faces():
        xyz = np.array(a.face_coordinates(face))
        # Face center & normal data
        o = np.mean(xyz, axis=0)
        w = np.array(a.face_normal(face))

        # Compute longest edge direction for stable local frame
        edge_vectors = xyz[1:] - xyz[:-1]
        if len(edge_vectors) == 0:
            continue  # Skip degenerate face
        longest_edge = max(edge_vectors, key=lambda e: np.linalg.norm(e))

        u = longest_edge
        v = cross_vectors(w, u)

        frames[face] = Frame(o, u, v)

    interfaces = []

    # -------------------------------------------------------------------------
    # 3. Loop over faces in A, transform all of B’s vertices once per face
    # -------------------------------------------------------------------------
    for f0, frame in frames.items():
        origin = frame.point
        uvw = np.array([frame.xaxis, frame.yaxis, frame.zaxis])
        A = uvw.astype(float)
        o = np.array(origin, dtype=float).reshape((-1, 1))

        # 3a) Transform face A’s coordinates (check for singular)
        a_xyz0 = np.array(a.face_coordinates(f0), dtype=float).T
        try:
            rst0 = solve(A.T, a_xyz0 - o).T
        except np.linalg.LinAlgError:
            # Skip if frame is degenerate
            continue

        p0 = Polygon(rst0.tolist())

        # 3b) Transform **all** B vertices in one shot
        try:
            rst_b = solve(A.T, b_xyz - o).T  # shape: (N_b_vertices, 3)
        except np.linalg.LinAlgError:
            continue

        # 3c) KD-tree to find nearby faces in B
        #     Use bounding box diagonal around face in A
        bbox_diag = np.linalg.norm(np.max(a_xyz0, axis=1) - np.min(a_xyz0, axis=1))
        search_radius = bbox_diag * 1.0  # Adjust for your geometry
        nearby_faces = tree.query_ball_point(a.face_center(f0), r=search_radius)
        if not nearby_faces:
            continue

        # ---------------------------------------------------------------------
        # 4. Check each nearby face in B
        # ---------------------------------------------------------------------
        for f1 in nearby_faces:
            # 4a) Sub-index already-transformed coords for B’s face f1
            indices_f1 = b_face_vertex_indices[f1]
            rst1 = rst_b[indices_f1]

            # 4b) Check planarity threshold
            if any(abs(t) > tmax for r, s, t in rst1):
                continue

            # 4c) Construct shapely Polygon & check area
            p1 = Polygon(rst1.tolist())
            if p1.area < amin:
                continue

            # 4d) Intersection with face A
            if not p0.intersects(p1):
                continue

            intersection = p0.intersection(p1)
            if intersection.is_empty:
                continue
            area = intersection.area
            if area < amin:
                continue

            # 4e) Build interface from intersection
            coords_2d = list(intersection.exterior.coords)[:-1]  # remove closing coordinate
            coords_2d_3 = [[xy[0], xy[1], 0.0] for xy in coords_2d]

            # Re-project intersection to 3D
            coords_3d = local_to_world_coordinates_numpy(Frame(o, A[0], A[1]), coords_2d_3).tolist()

            new_interface = Interface(
                size=area,
                points=coords_3d,
                frame=Frame(centroid_points(coords_3d), frame.xaxis, frame.yaxis),
            )
            interfaces.append(new_interface)

    return interfaces
