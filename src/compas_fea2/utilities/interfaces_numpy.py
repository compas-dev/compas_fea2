import numpy as np
from shapely.geometry import Polygon
from scipy.spatial import KDTree
from numpy.linalg import solve
from compas.geometry import Frame, centroid_points, cross_vectors, local_to_world_coordinates_numpy
from compas_fea2.model.interfaces import Interface


def face_bounding_sphere(mesh, face):
    """
    Compute a bounding sphere for a given face:
      center = average of face vertices
      radius = max distance from center to any vertex
    """
    coords = mesh.face_coordinates(face)
    if not coords:
        return None, 0.0
    center = np.mean(coords, axis=0)
    radius = max(np.linalg.norm(c - center) for c in coords)
    return center, radius


def mesh_mesh_interfaces(a, b, tmax=1e-6, amin=1e-1):
    """
    Face-face contact detection between two meshes, using
    broad-phase bounding spheres + narrow-phase 2D polygon intersection.

    Parameters
    ----------
    a : Mesh (compas.datastructures.Mesh)
    b : Mesh (compas.datastructures.Mesh)
    tmax : float
        Maximum allowable Z-deviation in the local frame.
    amin : float
        Minimum area for a valid intersection polygon.

    Returns
    -------
    List[Interface]
        A list of face-face intersection interfaces.
    """

    # ---------------------------------------------------------------------
    # 1. Precompute B’s data once
    # ---------------------------------------------------------------------
    b_xyz = np.array(b.vertices_attributes("xyz"), dtype=float).T
    k_i = {key: index for index, key in enumerate(b.vertices())}

    # We also store face center for each face in B (for the KDTree)
    faces_b = list(b.faces())
    face_centers_b = []
    face_radii_b = []
    face_vertex_indices_b = []

    for fb in faces_b:
        centerB, radiusB = face_bounding_sphere(b, fb)
        face_centers_b.append(centerB)  # bounding sphere center
        face_radii_b.append(radiusB)

        # Store the vertex indices for this face
        face_vs = b.face_vertices(fb)
        face_vertex_indices_b.append([k_i[vk] for vk in face_vs])

    face_centers_b = np.array(face_centers_b)
    face_radii_b = np.array(face_radii_b)

    # Build a KDTree for B’s face centers
    if len(face_centers_b) == 0:
        print("No faces in mesh B. Exiting.")
        return []

    # ---------------------------------------------------------------------
    # 2. Precompute A’s bounding spheres & KDTree
    # ---------------------------------------------------------------------
    faces_a = list(a.faces())
    face_centers_a = []
    face_radii_a = []
    frames_a = {}  # local 2D frames for each face in A (for narrow-phase)

    for fa in faces_a:
        centerA, radiusA = face_bounding_sphere(a, fa)
        face_centers_a.append(centerA)
        face_radii_a.append(radiusA)

        # Precompute stable local frame for face A
        coordsA = np.array(a.face_coordinates(fa))
        if coordsA.shape[0] < 2:
            continue
        w = np.array(a.face_normal(fa))
        edge_vecs = coordsA[1:] - coordsA[:-1]
        if len(edge_vecs) == 0:
            continue
        longest_edge = max(edge_vecs, key=lambda e: np.linalg.norm(e))

        u = longest_edge
        v = cross_vectors(w, u)

        frames_a[fa] = Frame(centerA, u, v)

    face_centers_a = np.array(face_centers_a)
    face_radii_a = np.array(face_radii_a)

    # KDTree for A’s face centers
    tree_a = KDTree(face_centers_a)

    # ---------------------------------------------------------------------
    # 3. Helper: 2D polygon from face in local frame
    # ---------------------------------------------------------------------
    def face_polygon_in_frame(mesh, face, frame):
        """
        Project a face into `frame`'s local XY, returning a shapely Polygon.
        """
        coords_3d = np.array(mesh.face_coordinates(face)).T
        A = np.array([frame.xaxis, frame.yaxis, frame.zaxis], dtype=float).T
        o = np.array(frame.point, dtype=float).reshape(-1, 1)

        try:
            rst = solve(A, coords_3d - o).T  # shape: (n,3), but z ~ 0
        except np.linalg.LinAlgError:
            return None
        # If the Z-values are large, it might fail tmax
        return Polygon(rst[:, :2])  # polygon in local 2D plane

    # ---------------------------------------------------------------------
    # 4. Narrow-phase intersection
    # ---------------------------------------------------------------------
    def intersect_faces(fa, fb):
        """
        Return an Interface if face fa intersects face fb, else None.
        """
        # bounding sphere overlap is already assumed; we do a final check for planarity + polygon intersection

        # local frame of face A
        fA_center, fA_radius = face_bounding_sphere(a, fa)
        frameA = frames_a.get(fa)
        if not frameA:
            return None

        # Build polygon for face A
        pA = face_polygon_in_frame(a, fa, frameA)
        if pA is None or pA.is_empty or pA.area < amin:
            return None

        # Transform all B vertices once for the frame of A:
        # But we only need face fb’s vertices
        # Instead, let's do a minimal local transform of face fb
        coords_3d_b = np.array(b.face_coordinates(fb)).T
        A_mat = np.array([frameA.xaxis, frameA.yaxis, frameA.zaxis], dtype=float).T
        o_mat = np.array(frameA.point, dtype=float).reshape(-1, 1)

        try:
            rst_b = solve(A_mat, coords_3d_b - o_mat).T
        except np.linalg.LinAlgError:
            return None

        # Check planarity threshold
        if any(abs(z) > tmax for x, y, z in rst_b):
            return None

        pB = Polygon(rst_b[:, :2])
        if pB.is_empty or pB.area < amin:
            return None

        if not pA.intersects(pB):
            return None

        intersection = pA.intersection(pB)
        if intersection.is_empty:
            return None
        area = intersection.area
        if area < amin:
            return None

        # Re-project intersection to 3D
        coords_2d = list(intersection.exterior.coords)[:-1]  # exclude closing point
        coords_2d_3 = [[x, y, 0.0] for x, y in coords_2d]

        coords_3d = local_to_world_coordinates_numpy(Frame(o_mat.ravel(), A_mat[:, 0], A_mat[:, 1]), coords_2d_3).tolist()

        return Interface(
            size=area,
            points=coords_3d,
            frame=Frame(centroid_points(coords_3d), frameA.xaxis, frameA.yaxis),
        )

    # ---------------------------------------------------------------------
    # 5. Broad-Phase + Narrow-Phase
    # ---------------------------------------------------------------------
    interfaces = []

    # A. For each face in B, find overlapping faces in A
    for idxB, fb in enumerate(faces_b):
        centerB = face_centers_b[idxB]
        radiusB = face_radii_b[idxB]

        # Search in A’s KDTree
        candidate_indices = tree_a.query_ball_point(centerB, r=radiusB + np.max(face_radii_a))

        for idxA in candidate_indices:
            centerA = face_centers_a[idxA]
            radiusA = face_radii_a[idxA]

            # Check actual bounding sphere overlap
            dist_centers = np.linalg.norm(centerB - centerA)
            if dist_centers > (radiusA + radiusB):
                continue  # No overlap in bounding sphere

            # Now do narrow-phase
            fa = faces_a[idxA]
            interface = intersect_faces(fa, fb)
            if interface:
                interfaces.append(interface)

    return interfaces
