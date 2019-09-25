import numpy as np
import math


def local_stifness(L, E, G, A, Ix, Iy, Iz):
    w1 = E * A / L
    w2 = 12 * E * Iz / (L * L * L)
    w3 = 6 * E * Iz / (L * L)
    w4 = 4 * E * Iz / L
    w5 = 2 * E * Iz / L
    w6 = 12 * E * Iy / (L * L * L)
    w7 = 6 * E * Iy / (L * L)
    w8 = 4 * E * Iy / L
    w9 = 2 * E * Iy / L
    w10 = G * Ix / L

    y = np.array([[w1, 0, 0, 0, 0, 0, -w1, 0, 0, 0, 0, 0],
                  [0, w2, 0, 0, 0, w3, 0, -w2, 0, 0, 0, w3],
                  [0, 0, w6, 0, -w7, 0, 0, 0, -w6, 0, -w7, 0],
                  [0, 0, 0, w10, 0, 0, 0, 0, 0, -w10, 0, 0],
                  [0, 0, -w7, 0, w8, 0, 0, 0, w7, 0, w9, 0],
                  [0, w3, 0, 0, 0, w4, 0, -w3, 0, 0, 0, w5],
                  [-w1, 0, 0, 0, 0, 0, w1, 0, 0, 0, 0, 0],
                  [0, -w2, 0, 0, 0, -w3, 0, w2, 0, 0, 0, -w3],
                  [0, 0, -w6, 0, w7, 0, 0, 0, w6, 0, w7, 0],
                  [0, 0, 0, -w10, 0, 0, 0, 0, 0, w10, 0, 0],
                  [0, 0, -w7, 0, w9, 0, 0, 0, w7, 0, w8, 0],
                  [0, w3, 0, 0, 0, w5, 0, -w3, 0, 0, 0, w4]])

    return y


def transformation_array(L, x1, y1, z1, x2, y2, z2, bt):
    cx = (x2 - x1) / L
    cy = (y2 - y1) / L
    cz = (z2 - z1) / L

    coa = math.cos(bt)
    sia = (1 - coa) ** 2
    up = (cx ** 2 + cz ** 2) ** 0.5

    if up != 0:
        m11 = cx
        m12 = cy
        m13 = cz
        m21 = (-cx * cy * coa - cz * sia) / up
        m22 = up * coa
        m23 = (-cy * cz * coa + cx * sia) / up
        m31 = (cx * cy * sia - cz * coa) / up
        m32 = -up * sia
        m33 = (cy * cz * sia + cx * coa) / up
    else:
        m11 = 0
        m12 = cy
        m13 = 0
        m21 = -cy * coa
        m22 = 0
        m23 = sia
        m31 = cy * sia
        m32 = 0
        m33 = coa

    Lambda = np.array([[m11, m12, m13],
                       [m21, m22, m23],
                       [m31, m32, m33]])

    LAMDA = np.zeros((12, 12))
    LAMDA[:3, :3], LAMDA[3:6, 3:6] = Lambda, Lambda
    LAMDA[6:9, 6:9], LAMDA[9:, 9:] = Lambda, Lambda
    return LAMDA


def global_stifness(nodes_N, elements):
    step = nodes_N * 6
    K_ol = np.zeros((step, step))
    for number, element in elements.items():
        slice1 = slice(element.dofi_1, element.dofi_2, 1)
        slice2 = slice(element.dofj_1, element.dofj_2, 1)
        k = element.stifness_glob
        K_ol[slice1, slice1] += k[:6, :6]
        K_ol[slice1, slice2] += k[:6, 6:]
        K_ol[slice2, slice1] += k[6:, :6]
        K_ol[slice2, slice2] += k[6:, 6:]

    return K_ol


def fixed_forces_point(transform, L, loads):
    A = np.zeros((12))
    if loads:
        for load in loads:
            p = transform.dot(np.array([load.px, load.py, load.pz, load.mx, load.my, load.mz]))
            a = load.c * L
            b = (1 - load.c) * L
            c = a / L
            d = b / L
            e = a ** 2 * b / L ** 2
            f = a * b ** 2 / L ** 2
            g = (d - e / L + f / L)
            h = (c + e / L - f / L)

            A[0] += -p[0] * (1 - load.c)
            A[6] += -p[0] * load.c
            A[1] += -p[1] * g
            A[7] += -p[1] * h
            A[2] += -p[2] * g
            A[8] += -p[2] * h
            A[3] += -p[3] * (1 - load.c)
            A[9] += -p[3] * load.c
            A[4] += p[2] * f
            A[10] += -p[2] * e
            A[5] += -p[1] * f
            A[11] += p[1] * e

    return A


def dist_load_fixed_forces(d_loads, transform, L):
    A = np.zeros((12))
    for load in d_loads:
        Fi, Mi, Fj, Mj = dist_load_reactions(load.c, load.l, load.py1, load.py2, L)
        A[1] += Fi
        A[7] += Fj
        A[5] += Mi
        A[11] += Mj

        Fi, Mi, Fj, Mj = dist_load_reactions(load.c, load.l, load.pz1, load.pz2, L)
        A[2] += Fi
        A[8] += Fj
        A[4] += Mi
        A[10] += Mj
    return A


def dist_load_reactions(c, l, p1, p2, L):
    w1 = p1
    w2 = p2
    s1 = c * L
    s2 = l * L
    s3 = L - s1 - s2
    temp1_Mi = w1 * s2 * (
            3 * s2 ** 3 + 15 * s2 ** 2 * s1 + 10 * s3 ** 2 * s2 + 30 * s3 ** 2 * s1 + 10 * s2 ** 2 * s3 + 40 * s1 * s2 * s3) / 60 / (
                       s1 + s2 + s3) ** 2
    temp2_Mi = w2 * s2 * (
            2 * s2 ** 3 + 5 * s2 ** 2 * s1 + 20 * s3 ** 2 * s2 + 30 * s3 ** 2 * s1 + 10 * s2 ** 2 * s3 + 20 * s1 * s2 * s3) / 60 / (
                       s1 + s2 + s3) ** 2

    Mi = temp1_Mi + temp2_Mi
    temp1_Mj = -w2 * s2 * (
            3 * s2 ** 3 + 15 * s2 ** 2 * s3 + 10 * s1 ** 2 * s2 + 30 * s1 ** 2 * s3 + 10 * s2 ** 2 * s1 + 40 * s1 * s2 * s3) / 60 / (
                       s1 + s2 + s3) ** 2
    temp2_Mj = -w1 * s2 * (
            2 * s2 ** 3 + 5 * s2 ** 2 * s3 + 20 * s1 ** 2 * s2 + 30 * s1 ** 2 * s3 + 10 * s2 ** 2 * s1 + 20 * s1 * s2 * s3) / 60 / (
                       s1 + s2 + s3) ** 2

    Mj = temp1_Mj + temp2_Mj

    temp1_Fi = w2 * s2 * (
            3 * s2 ** 3 + 5 * s2 ** 2 * s1 + 10 * s3 ** 3 + 30 * s3 ** 2 * s2 + 30 * s3 ** 2 * s1 + 15 * s2 ** 2 * s3 + 20 * s1 * s2 * s3) / 20 / (
                       s1 + s2 + s3) ** 3
    temp2_Fi = w1 * s2 * (
            7 * s2 ** 3 + 15 * s2 ** 2 * s1 + 10 * s3 ** 3 + 30 * s3 ** 2 * s2 + 30 * s3 ** 2 * s1 + 25 * s2 ** 2 * s3 + 40 * s1 * s2 * s3) / 20 / (
                       s1 + s2 + s3) ** 3

    Fi = temp1_Fi + temp2_Fi

    temp1_Fj = w1 * s2 * (
            3 * s2 ** 3 + 5 * s2 ** 2 * s3 + 10 * s1 ** 3 + 30 * s1 ** 2 * s2 + 30 * s1 ** 2 * s3 + 15 * s2 ** 2 * s1 + 20 * s1 * s2 * s3) / 20 / (
                       s1 + s2 + s3) ** 3
    temp2_Fj = w2 * s2 * (
            7 * s2 ** 3 + 15 * s2 ** 2 * s3 + 10 * s1 ** 3 + 30 * s1 ** 2 * s2 + 30 * s1 ** 2 * s3 + 25 * s2 ** 2 * s1 + 40 * s1 * s2 * s3) / 20 / (
                       s1 + s2 + s3) ** 3

    Fj = temp1_Fj + temp2_Fj

    return Fi, Mi, Fj, Mj


def rearrangement(array, dofs):
    step = len(dofs)
    tmp = np.arange(step)  # [i for i in range(48)]
    V = np.zeros((step, step))
    V[tmp, dofs] = 1
    if array.shape[1] == 1:
        a = V.dot(array)
    else:
        a = V.dot(array).dot(np.transpose(V))

    return a


def argsort(seq):
    return sorted(range(len(seq)), key=seq.__getitem__)
