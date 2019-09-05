import numpy as np
import math
import pandas as pd
# from sqlalchemy import create_engine
import time
import copy
from sqlalchemy import create_engine


def load_data(user_id, engine):
    # elements = pd.read_csv('model_test/test_1/elements.csv')
    truss_elements = pd.read_csv('model_test/test_1/truss_elements.csv')
    # nodes = pd.read_csv('model_test/test_1/nodes.csv')

    # point_loads = pd.read_csv('model_test/test_1/point_loads.csv')
    # dist_loads = pd.read_csv('model_test/test_1/dist_loads.csv')

    nodes = pd.read_sql("SELECT * from nodes WHERE user_id='" + user_id + "'", engine).sort_values(
        by=['number']).reset_index()
    del nodes['index']
    elements = pd.read_sql("SELECT * from elements WHERE user_id='" + user_id + "'", engine)
    sections = pd.read_sql("SELECT * from sections WHERE user_id='" + user_id + "'", engine)
    materials = pd.read_sql("SELECT * from materials WHERE user_id='" + user_id + "'", engine)
    point_loads = pd.read_sql("SELECT * from point_loads WHERE user_id='" + user_id + "'", engine)
#    del point_loads['id']
    # sections = pd.read_csv('model_test/test_1/sections.csv')
    dist_loads = pd.read_sql("SELECT * from dist_loads WHERE user_id='" + user_id + "'", engine)
    temp_loads_group = point_loads.groupby(['number', 'c'])
    temp_load = []
    for t in temp_loads_group:
        number = t[0][0]
        c = t[0][1]
        p_x, p_y, p_z, m_x, m_y, m_z = 0, 0, 0, 0, 0, 0
        for index, load in t[1].iterrows():
            p_x += load.p_x
            p_y += load.p_y
            p_z += load.p_z
            m_x += load.m_x
            m_y += load.m_y
            m_z += load.m_z
        temp_load.append((user_id, number, c, p_x, p_y, p_z, m_x, m_y, m_z))
        # df = pd.DataFrame([temp_load], columns=point_loads.columns)
    point_loads_new = pd.DataFrame(temp_load, columns=point_loads.columns)
    return elements, nodes, sections, materials, point_loads_new, dist_loads, truss_elements


# calculate DOFS
def dofs(nodes):
    t1 = time.time()
    nodes_n = len(nodes)
    #   #get 1D array of the constraints
    constraints = nodes.iloc[:, [6, 7, 8, 9, 10, 11]].get_values().flatten(order='C')
    #   #argsort returns the indexes to sort the constraints to free and sup
    dofs = constraints.argsort()
    node_dofs = pd.DataFrame(np.reshape(np.sort(dofs), (nodes_n, 6)))
    node_dofs['number'] = nodes['number']
    node_dofs.columns = ['dof_dx', 'dof_dy', 'dof_dz', 'dof_rx', 'dof_ry', 'dof_rz', 'number']
    a = constraints[constraints.argsort()]
    temp = np.where(a == 0)
    slice = temp[0][len(temp[0]) - 1] + 1
    sup_dofs = sorted(dofs[:slice].tolist())
    free_dofs = sorted(dofs[slice:].tolist())
    arranged_dofs = free_dofs + sup_dofs
    print('DOFS: ', time.time() - t1)
    return arranged_dofs, free_dofs, sup_dofs, node_dofs


def stifness_array(dofs, elements, nodes, sections, materials, node_dofs, truss_elements):
    local_stifness = []
    transf_arrays = []
    step = len(nodes) * 6
    K_ol = np.zeros((step, step))
    t1_, t2_, t3_, t4_ = 0, 0, 0, 0
    for index, elm in elements.iterrows():
        check1 = nodes.number == elm.nodei
        check2 = nodes.number == elm.nodej
        nodei = nodes.loc[check1]
        nodej = nodes.loc[check2]
        sect = sections.loc[sections.section_id == elm.section_id]
        material = materials.loc[materials.material_id == sect.material.values[0]]
        k = local_stif(elm, sect, material)
        # for releases will just make the stifness zero
        # 1 stands for released
        fixity = elm.iloc[8:].get_values()
        released_indices = np.where(fixity != 0)

        k[:, released_indices] = 0
        k[released_indices, :] = 0

        local_stifness.append(k.copy())
        rot = transformation_array(elm, nodei, nodej)
        transf_arrays.append(rot.copy())
        t = np.transpose(rot).dot(k).dot(rot)
        temp = time.time()
        i = nodei.number.get_values()[0]
        j = nodej.number.get_values()[0]

        dofs_i = node_dofs.loc[node_dofs.number == i]
        dofs_j = node_dofs.loc[node_dofs.number == j]
        dof_a, dof_b = dofs_i['dof_dx'].get_values()[0], \
                       dofs_i['dof_rz'].get_values()[0] + 1
        dof_c, dof_d = dofs_j['dof_dx'].get_values()[0], \
                       dofs_j['dof_rz'].get_values()[0] + 1
        t1_ += (time.time() - temp)
        K_ol[dof_a:dof_b, dof_a:dof_b] += t[:6, :6]
        K_ol[dof_a:dof_b, dof_c:dof_d] += t[:6, 6:]
        K_ol[dof_c:dof_d, dof_a:dof_b] += t[6:, :6]
        K_ol[dof_c:dof_d, dof_c:dof_d] += t[6:, 6:]

    return local_stifness, transf_arrays, K_ol


def local_stif(element, sect, material):
    L = element.length
    elem_type = element.elem_type
    A = sect.A.get_values()[0]  # 0.2090318
    E = material.E.get_values()[0]  # 200000000  # 199948023.75
    if elem_type == 'beam':
        Iy, Iz, G, J = sect.Iy.get_values()[0], sect.Iz.get_values()[0], material.G.get_values()[0], \
                       sect.Ix.get_values()[0]
        w1 = E * A / L
        w2 = 12 * E * Iz / (L * L * L)
        w3 = 6 * E * Iz / (L * L)
        w4 = 4 * E * Iz / L
        w5 = 2 * E * Iz / L
        w6 = 12 * E * Iy / (L * L * L)
        w7 = 6 * E * Iy / (L * L)
        w8 = 4 * E * Iy / L
        w9 = 2 * E * Iy / L
        w10 = G * J / L

        y = np.zeros((12, 12))
        # creates half the stifness matrix

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


    else:
        w1 = E * A / L
        y = np.array([[w1, 0, 0, -w1, 0, 0],
                      [0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0],
                      [-w1, 0, 0, w1, 0, 0],
                      [0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0]])

    return y


def transformation_array(element, nodei, nodej):
    L = element.length
    i, j = element.nodei, element.nodej
    bt = 0
    x1, x2 = nodei.coord_x.get_values()[0], nodej.coord_x.get_values()[0]
    y1, y2 = nodei.coord_y.get_values()[0], nodej.coord_y.get_values()[0]
    z1, z2 = nodei.coord_z.get_values()[0], nodej.coord_z.get_values()[0]
    # need to find what works for the random case
    #

    cx = (x2 - x1) / L
    cy = (y2 - y1) / L
    cz = (z2 - z1) / L

    coa = math.cos(bt)
    sia = ((1 - coa) ** 2)
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

    '''
    plane = 'xyz'
    helpVector = np.array([0, 1, 0])
    dirVector = np.array([CXx, CYx, CZx])
    if (CXx != 0 and CYx == 0):
        zLocal = np.cross(dirVector, helpVector)
        yLocal = np.cross(zLocal, dirVector)
    elif (CXx == 0 and CYx != 0):
        plane = 'yz'
    elif (CZx == 0 and CXx != 0 and CYx != 0):
        plane = 'xy'
    elif (CXx == 0 and CYx == 0):
        zLocal = np.array([-1, 0, 0])
        yLocal = np.array([0, 1, 0])
    xR, yR, zR = 0, 1, 0

    Lambda = np.zeros((3, 3))
    if element.elem_type == 'beam':
        if CXx == 0 and CZx == 0:
            Y = -xR + x1
            Z = zR - z1
            if y1 > y2:
                Y = -Y

        else:
            SQ = math.sqrt(CXx * CXx + CZx * CZx)
            Y = -CXx * CYx * (xR - x1) / SQ + SQ * (yR - y1) - CYx * CZx * (zR - z1) / SQ
            Z = -CZx * (xR - x1) / SQ + CXx * (zR - z1) / SQ

        SQyz = math.sqrt(Y * Y + Z * Z)
        SINY = Z / SQyz
        COSY = Y / SQyz

        Lambda[0, 0] = CXx
        Lambda[0, 1] = CYx
        Lambda[0, 2] = CZx
        if CXx == 0 and CZx == 0:

            Lambda[1, 0] = -COSY
            Lambda[1, 1] = 0
            Lambda[1, 2] = SINY
            Lambda[2, 0] = SINY
            Lambda[2, 1] = 0
            Lambda[2, 2] = COSY
            if y1 >= y2:
                Lambda[1, 0] = COSY
                Lambda[2, 0] = -SINY
        else:
            Lambda[1, 0] = -(CXx * CYx * COSY + CZx * SINY) / SQ
            Lambda[1, 1] = SQ * COSY
            Lambda[1, 2] = -(CYx * CZx * COSY - CXx * SINY) / SQ
            Lambda[2, 0] = (CXx * CYx * SINY - CZx * COSY) / SQ
            Lambda[2, 1] = -SQ * SINY
            Lambda[2, 2] = (CYx * CZx * SINY + CXx * COSY) / SQ
    '''
    LAMDA = np.zeros((12, 12))

    LAMDA[:3, :3], LAMDA[3:6, 3:6] = Lambda, Lambda
    LAMDA[6:9, 6:9], LAMDA[9:, 9:] = Lambda, Lambda
    return LAMDA


def nodal_forces(point_loads, dist_loads, node_dofs, tranf_arrays, arranged_dofs, elements):
    t = time.time()

    P_nodal = np.zeros((len(arranged_dofs), 1))
    S = np.zeros((len(arranged_dofs), 1))
    fixed_forces = np.zeros((12, len(elements)))

    for index, load in point_loads.iterrows():
        A = np.zeros((12, 1))

        if load.c == 99999:

            node = load.number
            a, b = node_dofs.loc[node_dofs.number == node]['dof_dx'].get_values()[0], \
                   node_dofs.loc[node_dofs.number == node]['dof_rz'].get_values()[0] + 1
            P_nodal[a:b] += [[load.p_x], [load.p_y], [load.p_z],
                             [load.m_x], [load.m_y], [load.m_z]]
        else:
            elm_id = load.number
            elm = elements.loc[elements.number == elm_id]
            L = elm.length.get_values()[0]

            fixity = elm.iloc[8:].get_values()
            released_indices = np.where(fixity != 0)

            nodei = elm.nodei.get_values()[0]
            nodej = elm.nodej.get_values()[0]
            dofa, dofb = node_dofs.loc[node_dofs.number == nodei]['dof_dx'].get_values()[0], \
                         node_dofs.loc[node_dofs.number == nodei]['dof_rz'].get_values()[0] + 1
            dofc, dofd = node_dofs.loc[node_dofs.number == nodej]['dof_dx'].get_values()[0], \
                         node_dofs.loc[node_dofs.number == nodej]['dof_rz'].get_values()[0] + 1
            a = load.c * L
            b = (1 - load.c) * L
            # add the appropriate moment loads
            p = load.iloc[[3, 4, 5, 6, 7, 8]].get_values()

            A[0] = -p[0] * (1 - load.c)  # Fx_i
            A[6] = -p[0] * load.c  # Fx_j
            A[1] = -p[1] * (b / L - a ** 2 * b / L ** 3 + a * b ** 2 / L ** 3)  # Fy_i
            A[7] = -p[1] * (a / L + a ** 2 * b / L ** 3 - a * b ** 2 / L ** 3)  # Fy_j
            A[2] = -p[2] * (b / L - a ** 2 * b / L ** 3 + a * b ** 2 / L ** 3)  # Fz_i
            A[8] = -p[2] * (a / L + a ** 2 * b / L ** 3 - a * b ** 2 / L ** 3)  # Fz_j
            A[3] = -p[3] * (1 - load.c)  # Mx_i
            A[9] = -p[3] * load.c  # Mx_j
            A[4] = p[2] * a * b ** 2 / L ** 2  # My_i
            A[10] = -p[2] * a ** 2 * b / L ** 2  # My_j
            A[5] = -p[1] * a * b ** 2 / L ** 2  # Mz_i
            A[11] = p[1] * a ** 2 * b / L ** 2  # Mz_j

            # element forces from to local to global
            A[released_indices] = 0
            rot = tranf_arrays[elm.index[0]][:6, :6]

            S[dofa:dofb] += np.transpose(rot).dot(A[:6])
            S[dofc:dofd] += np.transpose(rot).dot(A[6:])
            fixed_forces[:6, elm.index[0]] = np.reshape(A[:6], 6)
            fixed_forces[6:, elm.index[0]] = np.reshape(A[6:], 6)
    # approaching dist loads adding two triangle loads: (p1,0) + (0,p2)0
    for index, d_load in dist_loads.iterrows():
        A = np.zeros((12, 1))

        elm_id = d_load.number
        elm = elements.loc[elements.number == elm_id]
        fixity = elm.iloc[0][8:].get_values()
        released_indices = np.where(fixity != 0)
        L = elm.length.get_values()[0]

        nodei = elm.nodei.get_values()[0]
        nodej = elm.nodej.get_values()[0]
        dofa, dofb = node_dofs.loc[node_dofs.number == nodei]['dof_dx'].get_values()[0], \
                     node_dofs.loc[node_dofs.number == nodei]['dof_rz'].get_values()[0] + 1
        dofc, dofd = node_dofs.loc[node_dofs.number == nodej]['dof_dx'].get_values()[0], \
                     node_dofs.loc[node_dofs.number == nodej]['dof_rz'].get_values()[0] + 1

        p = d_load.iloc[[3, 4, 5, 6, 7, 8]].get_values()

        Fi, Mi, Fj, Mj = dist_load_reactions(d_load.c, d_load.l, d_load.p_1_z, d_load.p_2_z, L)
        A[2] = -Fi
        A[8] = -Fj

        A[4] = Mi
        A[10] = Mj

        A[released_indices] = 0
        rot = tranf_arrays[elm.index[0]][:6, :6]
        S[dofa:dofb] += np.transpose(rot).dot(A[:6])
        S[dofc:dofd] += np.transpose(rot).dot(A[6:])
        fixed_forces[:6, elm.index[0]] = np.reshape(A[:6], 6)
        fixed_forces[6:, elm.index[0]] = np.reshape(A[6:], 6)
    print('nodal forces: ', time.time() - t)
    return P_nodal, S, fixed_forces


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


def solver(K, P_nodal, dofs, dofs_arranged, free, S):
    # rearagment of the arrays
    K_m = rearrangment(K, dofs_arranged)
    P_m = rearrangment(P_nodal, dofs_arranged)
    S_m = rearrangment(S, dofs_arranged)

    P_f = P_m[:free] - S_m[:free]

    Kff = K_m[:free, :free]
    Ksf = K_m[free:, :free]

    D_f = np.linalg.inv(Kff).dot(P_f)
    P_s = np.dot(Ksf, D_f) + S_m[free:]

    D = np.zeros((len(dofs), 1))
    i = 0
    for r in dofs_arranged[:free]:
        D[r] = D_f[i]
        i += 1

    return P_s, D


def rearrangment(array, dofs):
    step = len(dofs)
    anad = np.zeros((step, step))
    for i in range(len(dofs)):
        anad[i, dofs[i]] = 1
    if array.shape[1] == 1:
        a = anad.dot(array)
    else:
        a = anad.dot(array).dot(np.transpose(anad))

    return a


def nodal_mqn(K, Lamda, displacments, elements, node_dofs, S, nodes, point_loads, fixed_forces):
    mqn = []
    disp_local = []
    df = pd.DataFrame([])
    for index, elm in elements.iterrows():
        i = index

        sect = None
        nodei = nodes.loc[nodes.number == elm.nodei]
        nodej = nodes.loc[nodes.number == elm.nodej]
        k = K[index]

        rot = Lamda[index]

        nodei = elm.nodei
        nodej = elm.nodej

        a, b = node_dofs.loc[node_dofs.number == nodei]['dof_dx'].get_values()[0], \
               node_dofs.loc[node_dofs.number == nodei]['dof_rz'].get_values()[0] + 1
        c, d = node_dofs.loc[node_dofs.number == nodej]['dof_dx'].get_values()[0], \
               node_dofs.loc[node_dofs.number == nodej]['dof_rz'].get_values()[0] + 1
        d_elem = np.zeros((12, 1))
        d_elem[:6], d_elem[6:] = displacments[a:b], displacments[c:d]
        # local displacments
        d_local = rot.dot(d_elem)

        MQN = k.dot(d_local)

        check = np.zeros(12)
        fixity = elm.iloc[8:].get_values()
        released_indices = np.where(check != fixity)

        MQN[:6, 0] += fixed_forces[:6, index]
        MQN[6:, 0] += fixed_forces[6:, index]
        MQN[released_indices] = 0
        # need to add nodal forces from fixed elements
        mqn.append(MQN)
        disp_local.append(d_local)
        dt = pd.DataFrame(MQN)
        dt['number'] = elm.number
        df = pd.concat([df, dt])
    return mqn, disp_local


def rotate_loads(elements, point_loads, dist_loads, transf_arrays):
    point_loads_loc = []
    dist_loads_loc = []
    for index, p_load in point_loads.iterrows():
        check = (elements['number'] == p_load.number) & (p_load.c != 99999)
        elm = elements.loc[check]
        P = np.array([p_load.p_x, p_load.p_y, p_load.p_z, p_load.m_x, p_load.m_y, p_load.m_z])
        rot = transf_arrays[elm.index.get_values()[0]][:6, :6]
        p = rot.dot(P)
        point_loads_loc.append((p_load.user_id, p_load.number, p_load.c, p[0], p[1], p[2], p[3], p[4], p[5]))

    point_loads_local = pd.DataFrame(point_loads_loc, columns=point_loads.columns)

    nodal_point_loads = point_loads.loc[(point_loads.c == 99999)]
    point_loads_local = pd.concat([point_loads_local, nodal_point_loads])

    for index, d_load in dist_loads.iterrows():
        check = (elements['number'] == d_load.number)
        elm = elements.loc[check]
        P1 = np.array([d_load.p_1_x, d_load.p_1_y, d_load.p_1_z])
        P2 = np.array([d_load.p_2_x, d_load.p_2_y, d_load.p_2_z])

        rot = transf_arrays[elm.index.get_values()[0]][:3, :3]
        p1 = rot.dot(P1)
        p2 = rot.dot(P2)
        dist_loads_loc.append(
            (index + 1, d_load.user_id, d_load.number, p1[0], p2[0], p1[1], p2[1], p1[2], p2[2], d_load.c, d_load.l,
             'd_load'))

    dist_loads_local = pd.DataFrame(dist_loads_loc, columns=dist_loads.columns)

    return point_loads_local, dist_loads_local


def dist_to_pload(element, d_load, number):
    SP = d_load.p_1_z * d_load.l * element.length
    Pi = SP.get_values()[0] / number
    c = d_load.c.get_values()[0]
    dx = d_load.l.get_values()[0] / number
    loads = []
    elm = d_load.number.get_values()[0]
    user_id = d_load['user_id'].get_values()[0]
    for i in range(number):
        p = Pi
        pload = (0, user_id, elm, c, 0, 0, Pi, 0, 0, 0)
        loads.append(pload)
        print(c)
        c += dx

    return loads


def mqn_member(elements, MQN_nodes, point_loads, dist_loads, n):
    time1 = time.time()
    mqn_values = []
    for index, element in elements.iterrows():
        mqn_nodes = MQN_nodes[index]
        q_i = mqn_nodes[:6]
        q_j = mqn_nodes[6:]
        L = element.length

        Fxi, Fyi, Fzi = q_i[0], -q_i[1], q_i[2]
        Mxi, Myi, Mzi = q_i[3], q_i[4], q_i[5]
        Fxj, Fyj, Fzj = q_j[0], q_j[1], q_j[2]
        Mxj, Myj, Mzj = q_j[3], q_j[4], q_j[5]

        check1 = (point_loads.number == element.number) & (point_loads.c != 99999)
        check2 = (dist_loads.number == element.number)
        p_loads = point_loads.loc[check1]
        d_loads = dist_loads.loc[check2]

        x_dist = np.linspace(d_loads.c.get_values(), d_loads.l.get_values(), n)

        seg = x_dist[-1, :] - x_dist[0, :]
        seg = L * seg

        p = np.linspace(d_loads.p_1_z.get_values() * seg / n, d_loads.p_1_z.get_values() * seg / n, n)

        x_dist = x_dist.flatten('F') * L
        p = p.flatten('F')

        number = len(p)

        ploads = len(p_loads)
        pz = np.zeros((number + ploads * 2, 7))

        a = number + ploads
        pz[:number, 0] = x_dist
        pz[:number, 1] = p
        pz[number:a, 0] = p_loads.c.get_values() * L
        pz[number:a, 1] = p_loads.p_z.get_values()
        pz[number:a, 2] = p_loads.p_y.get_values()
        pz[number:a, 3] = p_loads.p_x.get_values()
        pz[number:a, 4] = p_loads.m_x.get_values()
        pz[number:a, 5] = p_loads.m_y.get_values()
        pz[number:a, 6] = p_loads.m_z.get_values()
        pz[a:, 0] = pz[number:number + ploads, 0] - 0.001
        pz[a:, 1] = 0

        pz = pz[pz[:, 0].argsort()]

        temp = np.zeros(len(pz) + 2)
        temp[0] = Fzi
        temp[1:-1] = pz[:, 1]
        Qz = np.cumsum(temp)

        temp = np.zeros(len(pz) + 2)
        temp[0] = Fyi
        temp[1:-1] = pz[:, 2]
        Qy = np.cumsum(temp)

        temp = np.zeros(len(pz) + 2)
        temp[0] = Fxi
        temp[1:-1] = pz[:, 3]
        Nx = np.cumsum(temp)

        temp = np.zeros(len(pz) + 2)
        temp[0] = Mxi
        temp[1:-1] = pz[:, 4]
        Mx = np.cumsum(temp)

        x = np.zeros(len(pz) + 2)

        x[1:-1] = np.diff(pz[:, 0], n=0)

        x[-1] = L

        dx = np.diff(x, n=1)

        my = np.zeros(len(pz) + 2)
        my[0] = Myi
        my[1:] += dx * Qz[1:]
        my = np.cumsum(my)
        # my[-1] = Myj

        temp = np.zeros(len(pz) + 2)
        temp[0] = Mzi
        temp[1:] += Qy[1:] * dx
        mz = np.cumsum(temp)
        # mz[-1] = Mzj

        t = np.zeros((len(x), 8))
        t[:, 0] = element.number
        t[:, 1] = x
        t[:, 2] = Nx
        t[:, 3] = Qy
        t[:, 4] = Qz
        t[:, 5] = Mx
        t[:, 6] = my
        t[:, 7] = mz

        mqn_values.append(t)

    t1 = np.concatenate(mqn_values[:])

    mqn = pd.DataFrame(t1, columns=['number', 'x', 'Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz'])
    print('mqn mebmers: ', time.time() - time1)
    return mqn


def displ_member(nodes, elements, local_displacements, global_dispalecements, transf_arrays, node_dofs):
    n = 50

    dd = np.zeros((n * len(elements), 4))

    for index, element in elements.iterrows():
        # local displacements

        nodei = nodes.loc[nodes.number == int(element.nodei)]
        nodej = nodes.loc[nodes.number == int(element.nodej)]
        L = element.length
        x1, x2 = nodei.coord_x.get_values()[0], nodej.coord_x.get_values()[0]
        y1, y2 = nodei.coord_y.get_values()[0], nodej.coord_y.get_values()[0]
        z1, z2 = nodei.coord_z.get_values()[0], nodej.coord_z.get_values()[0]
        # need to find what works for the random case
        #

        cx = (x2 - x1) / L
        cy = (y2 - y1) / L
        cz = (z2 - z1) / L

        global_x = np.linspace(nodei.coord_x, nodej.coord_x, n)
        global_y = np.linspace(nodei.coord_y, nodej.coord_y, n)
        global_z = np.linspace(nodei.coord_z, nodej.coord_z, n)

        rot = transf_arrays[index][:3]
        d_local = np.zeros((n, 4))
        L = element.length
        x = np.linspace(0, L, n)

        # z
        d = local_displacements[index]

        # local
        dx = 0.2
        xA = 0
        yA = d[2]
        xA_ = dx
        yA_ = yA - dx * math.tan(d[4])
        xB = L
        yB = d[8]
        xB_ = L - dx
        yB_ = yB + dx * math.tan(d[10])
        # fit me 3rd order polyonimial
        coef = np.polyfit([xA, xA_, xB_, xB], [yA, yA_, yB_, yB], 3)
        d_z = x ** 3 * coef[0] + x ** 2 * coef[1] + x * coef[2] + coef[3]

        dx = 0.2
        xA = 0
        yA = d[1]
        xA_ = dx
        yA_ = yA + dx * math.tan(d[5])
        xB = L
        yB = d[7]
        xB_ = L - dx
        yB_ = yB - dx * math.tan(d[11])
        # fit me 3rd order polyonimial
        coef = np.polyfit([xA, xA_, xB_, xB], [yA, yA_, yB_, yB], 3)
        d_y = x ** 3 * coef[0] + x ** 2 * coef[1] + x * coef[2] + coef[3]

        d_local[:, 0] = element.number
        d_local[:, 1] = x
        d_local[:, 2] = d_y
        d_local[:, 3] = d_z
        slic1 = index * n
        slic2 = slic1 + n
        dd[slic1:slic2] = d_local

        #global deformations



        # df = pd.DataFrame(d_local, columns=['number', 'x', 'u_y', 'u_z'])
        # D_LOCAL = pd.concat([D_LOCAL, df], axis=0).reset_index(drop=True)

    D_LOCAL = pd.DataFrame(dd, columns=['number', 'x', 'uy', 'uz'])

    D_GLOBAL = []
    return D_LOCAL, D_GLOBAL


def fit_points(num_points, **kwargs):
    columns = list(kwargs)
    d_t = pd.DataFrame([], columns=['x_Fx', 'Fx', 'x_Fy', 'Fy', 'x_Fz', 'Fz', 'x_Mx', 'Mx', 'x_My', 'My', 'x_Mz', 'Mz'])

    for key in kwargs.keys():
        X_whole = np.zeros((num_points * len(kwargs[key])))
        values_whole = np.zeros((num_points * len(kwargs[key])))
        # d_t = pd.DataFrame([], columns=df.columns)
        i = 0
        j = 10
        for segment in kwargs[key]:
            x_ = segment[0]
            y_ = segment[1]
            a, b = x_[0], x_[-1]
            if len(x_) < 4:
                degree = 1
            else:
                degree = 3
            x = np.linspace(a, b, num_points)
            coef = np.polyfit(x_, y_, degree)
            if degree == 1:
                values = x * coef[0] + coef[1]
            else:
                values = x ** 3 * coef[0] + x ** 2 * coef[1] + x * coef[2] + coef[3]
            X_whole[i:j] = np.round(x, 4)
            values_whole[i:j] = np.round(values, 4)
            i = j
            j += 10

        d_t[key] = values_whole
        d_t['x_' + str(key)] = X_whole
    # df = pd.concat([df, d_t], ignore_index=True)
    return d_t


def assign_reactions(user_id, nodes, P_whole, node_dofs, arranged_dofs):
    reactions = pd.DataFrame(columns=['user_id', 'number', 'Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz'])
    for index, node in node_dofs.iterrows():
        dofs = [node.dof_dx, node.dof_dy, node.dof_dz, node.dof_rx, node.dof_ry, node.dof_rz]
        ind_fx = dofs[0]  # arranged_dofs.index(node.dof_dx)
        ind_fy = dofs[1]  # arranged_dofs.index(node.dof_dy)
        ind_fz = dofs[2]  # arranged_dofs.index(node.dof_dz)
        ind_mx = dofs[3]  # arranged_dofs.index(node.dof_rx)
        ind_my = dofs[4]  # arranged_dofs.index(node.dof_ry)
        ind_mz = dofs[5]  # arranged_dofs.index(node.dof_rz)
        Fx = P_whole[ind_fx][0]
        Fy = P_whole[ind_fy][0]
        Fz = P_whole[ind_fz][0]
        Mx = P_whole[ind_mx][0]
        My = P_whole[ind_my][0]
        Mz = P_whole[ind_mz][0]

        temp_react = {'Fx': Fx, 'Fy': Fy, 'Fz': Fz, 'Mx': Mx, 'My': My, 'Mz': Mz}
        df = pd.DataFrame([temp_react], columns=temp_react.keys())
        # drops lines with zeroes
        df = df[(df.T != 0).any()]
        df['user_id'] = user_id
        df['number'] = node.number
        reactions = pd.concat([reactions, df], axis=0, sort=False).reset_index(drop=True)
    return reactions


def save_results(user_id, engine, **kwargs):
    for key in kwargs.keys():
        sql_stmt = "DELETE FROM " + key + " WHERE user_id='" + user_id + "'"
        with engine.connect() as con:
            con.execute(sql_stmt)
        kwargs[key].to_sql(key, engine, schema='yellow', if_exists='append', index=False, index_label=True,
                           chunksize=None, dtype=None)


def plot_results(user_id, mqn, displacements):
    from plots import plot_mqn, plot_displacements
    plot_mqn(user_id, mqn)
    plot_displacements(user_id, displacements)

def calculate_denco(d, nodes):

    nodei = nodes.loc[nodes.number==1]
    nodej = nodes.loc[nodes.number ==2]

    xi = nodei.coord_x.get_values() + d[0]
    yi = nodei.coord_y.get_values() + d[1]
    zi = nodei.coord_z.get_values() + d[2]
    xj = nodej.coord_x.get_values() + d[6]
    yj = nodej.coord_y.get_values() + d[7]
    zj = nodej.coord_z.get_values() + d[8]

    cos1 = math.cos(d[3])
    cos2 = math.cos(d[4])
    cos3 = math.cos(d[5])
    cos4 = math.cos(d[9])
    cos5 = math.cos(d[10])
    cos6 = math.cos(d[11])

    sin1 = math.sin(d[3])
    sin2 = math.sin(d[4])
    sin3 = math.sin(d[5])
    sin4 = math.sin(d[9])
    sin5 = math.sin(d[10])
    sin6 = math.sin(d[11])

    a = (xj * cos3 - yj * sin3) + (xj * cos2 + zj * sin2) + xj
    b = (xj * sin3 - yj * cos3) + (yj * cos1 - zj * sin1) + yj
    c = (-xj * sin2 + zj * cos2) + (yj * sin1 + zj * cos1) + zj

    e = (xi * cos6 - yi * sin6) + (xi * cos5 + zi * sin5) + xi
    f = (xi * sin6 - yi * cos6) + (yi * cos4 - zi * sin4) + yi
    dd = (-xi * sin5 + zi * cos5) + (yi * sin4 + zi * cos4) + zi

    K = np.array([a,b,c])
    L = np.array([e,f,dd])
    return None

def main(user_id, engine):
    t_whole = time.time()
    t = time.time()
    elements, nodes, sections, materials, point_loads, dist_loads, truss_elements = load_data(user_id, engine)
    print('load data: ', time.time() - t)
    arranged_dofs, free_dofs, sup_dofs, node_dofs = dofs(nodes)

    t = time.time()
    local_stifness, transf_arrays, K_ol = stifness_array(dofs, elements, nodes, sections, materials, node_dofs,
                                                         truss_elements)
    print('stif arrays: ', time.time() - t)
    t = time.time()
    point_loads_tr, dist_loads_tr = rotate_loads(elements, point_loads, dist_loads, transf_arrays)
    print('rotate loads: ', time.time() - t)
    t = time.time()
    P_nodal, S, fixed_forces = nodal_forces(point_loads_tr, dist_loads_tr, node_dofs, transf_arrays, arranged_dofs,
                                            elements)
    print('nodal_forces: ', time.time() - t)
    t = time.time()
    P_s, global_dispalecements = solver(K_ol, P_nodal, arranged_dofs, arranged_dofs, len(free_dofs), S)
    print('solver: ', time.time() - t)
    t = time.time()
    MQN_nodes, local_displacements = nodal_mqn(local_stifness, transf_arrays, global_dispalecements, elements,
                                               node_dofs, S, nodes,
                                               point_loads, fixed_forces)
    print('nodal_mqn: ', time.time() - t)
    t = time.time()
    MQN_values = mqn_member(elements, MQN_nodes, point_loads_tr, dist_loads_tr, 300)
    print('member: ', time.time() - t)
    t = time.time()
    d_local, d_global = displ_member(nodes, elements, local_displacements, global_dispalecements, transf_arrays,
                                     node_dofs)
    print('displacements: ', time.time() - t)
    MQN_values['user_id'] = user_id
    d_local['user_id'] = user_id
    P_whole = np.round(K_ol.dot(global_dispalecements) + S - P_nodal, 3)
    reactions = assign_reactions(user_id, nodes, P_whole, node_dofs, arranged_dofs)
    calculate_denco(global_dispalecements[:12], nodes)
    save_results(user_id, engine, mqn=MQN_values, displacements=d_local, reactions=reactions)
    print('not plots: ', time.time() - t_whole)
    # plot_results(user_id, MQN_values, d_local)
    print('whole: ', time.time() - t_whole)


    MQN_values.to_csv('model_test/test_1/mqn.csv')
    # global_dispalecements = pd.DataFrame(global_dispalecements)# .tosup_dofs)


# t1 = time.time()
# main('cv13116')
# print('Run: ', time.time() - t1)
'''
 # global dispalecements
        #
        number_i = int(node_i.number.get_values())
        number_j = int(node_j.number.get_values())
        # find the line coordinates x
        # direction vector
        x1, x2 = node_i.coord_x.get_values()[0], node_j.coord_x.get_values()[0]
        y1, y2 = node_i.coord_y.get_values()[0], node_j.coord_y.get_values()[0]
        z1, z2 = node_i.coord_z.get_values()[0], node_j.coord_z.get_values()[0]

        CXx = (x2 - x1) / L
        CYx = (y2 - y1) / L
        CZx = (z2 - z1) / L
        # print(1.3730472000000004e-05*rot[:,0])
        dof_a = (number_i-1)*6
        dof_b = number_i*6
        dof_c = (number_j-1)*6
        dof_d = number_j*6

        d_global = np.zeros((n, 4))

        x = np.linspace(0,L,n)
        # z

        d = global_dispalecements
        print(len(d))
        print(dof_a,dof_b)
        print(dof_c,dof_d)

        m2_A = d[dof_a:dof_b]
        m2_B = d[dof_c:dof_d]

        #
        # test sto z
        if index>0:
            dx = 0.2
            xA = 100*m2_A[0][0]
            yA = 0 # m2_A[2][0]
            xA_ = dx
            yA_ = dx*math.tan(m2_A[4][0])
            xB = L# +100*m2_B[0][0]
            yB = m2_B[2][0]
            xB_ = xB-dx
            yB_ = yB + dx*math.tan(m2_B[4][0])
            # fit me 3rd order polyonimial

            coef = np.polyfit([xA, xA_, xB_, xB],[yA, yA_, yB_, yB], 3)
            d_z = x**3*coef[0]+x**2*coef[1]+x*coef[2]+coef[3]
            print(m2_A[4][0], m2_B[4][0])
            # y
            dx = 0.2
            xA = 0# +100*m2_A[0][0]
            yA = m2_A[1]
            xA_ = dx
            yA_ = yA+dx*math.tan(m2_A[5])
            xB = L# +100*m2_B[0][0]
            yB = m2_B[1]
            xB_ = xB-dx
            yB_ = yB - dx*math.tan(m2_B[5])
            # fit me 3rd order polyonimial
            coef = np.polyfit([xA, xA_, xB_, xB ],[yA, yA_, yB_, yB], 3)
            d_y = x**3*coef[0]+x**2*coef[1]+x*coef[2]+coef[3]
        else:
            dx = 0.2
            xA = 100*m2_A[0][0]
            yA = m2_A[2][0]
            xA_ = dx
            yA_ = dx*math.tan(m2_A[4][0])
            xB = L+100*m2_B[0][0]
            yB = m2_B[2][0]
            xB_ = xB-dx
            yB_ = yB - dx*math.tan(m2_B[4][0])
            # fit me 3rd order polyonimial

            coef = np.polyfit([xA, xA_, xB_, xB],[yA, yA_, yB_, yB], 3)
            d_z = x**3*coef[0]+x**2*coef[1]+x*coef[2]+coef[3]

            # y
            dx = 0.2
            xA = 0+100*m2_A[0][0]
            yA = m2_A[1]
            xA_ = dx
            yA_ = yA+dx*math.tan(m2_A[5])
            xB = L+100*m2_B[0][0]
            yB = m2_B[1]
            xB_ = xB-dx
            yB_ = yB - dx*math.tan(m2_B[5])
            # fit me 3rd order polyonimial
            coef = np.polyfit([xA, xA_, xB_, xB ],[yA, yA_, yB_, yB], 3)
            d_y = x**3*coef[0]+x**2*coef[1]+x*coef[2]+coef[3]


        x_real = x1+CXx*x
        # x_real[n-1] +=100*m2_B[0][0]
        # x_real[0] +=100*m2_A[0][0]
        y_real = y1+CYx*x+100*d_y
        z_real = z1+CZx*x+100*d_z

        d_global[:, 0] = index+1
        d_global[:, 1] = x_real
        d_global[:, 2] = y_real
        d_global[:, 3] = z_reals
'''
