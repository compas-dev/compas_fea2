from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np


def principal_stresses(data):
    """Performs principal stress calculations solving the eigenvalues problem.

    Parameters
    ----------
    data : dic
        Element data from structure.results for the Step.

    Returns
    -------
    spr : dict
        dictionary with the principal stresses of each element organised per
        `stress_type` ('max', 'min') and `section_point` ('sp1, 'sp5').\n
        `{section_point: {stress_type: array([element_0, elemnt_1, ...])}}`
    e : dict
        dictionary with the principal stresses vector components in World coordinates
        of each element organised per `stress_type` ('max', 'min') and
        `section_point` ('sp1, 'sp5').\n
        `{section_point: {stress_type: array([element_0_x, elemnt_1_x, ...],[element_0_y, elemnt_1_y, ...])}}`

    Warnings
    --------
    The function is experimental and works only for shell elements at the moment.

    """
    components = ["sxx", "sxy", "syy"]
    stype = ["max", "min"]
    section_points = ["sp1", "sp5"]

    stress_results = list(zip(*[data[stress_name].values() for stress_name in components]))
    array_size = ((len(stress_results)), (2, len(stress_results)))
    spr, e = [{sp: {st: np.zeros(size) for st in stype} for sp in section_points} for size in array_size]

    for sp in section_points:
        for c, element_stresses in enumerate(stress_results):
            # Stresses are computed as mean of the values at each integration points
            stress_vector = [np.mean(np.array([v for k, v in i.items() if sp in k])) for i in element_stresses]
            # The principal stresses and their directions are computed solving the eigenvalues problem
            stress_matrix = np.array([(stress_vector[0], stress_vector[1]), (stress_vector[1], stress_vector[2])])
            w_sp, v_sp = np.linalg.eig(stress_matrix)
            # sort by larger to smaller eigenvalue
            idx = w_sp.argsort()[::-1]
            w_sp = w_sp[idx]
            v_sp = v_sp[:, idx]
            # populate results
            for v, k in enumerate(stype):
                spr[sp][k][c] += w_sp[v]
                e[sp][k][:, c] += v_sp[:, v]

    return spr, e
