import numpy as np
import math
import pandas as pd
from sqlalchemy import create_engine
import time
import copy


def load_data(user_id):
    engine = create_engine("mysql+pymysql://root:pass@localhost:3306/_0000125")
    elements = pd.read_sql('elements', engine)
    elements = elements.loc[elements['user_id'] == user_id]
    truss_elements = elements.loc[elements['elem_type'] == 'truss']
    nodes = pd.read_sql('nodes', engine)
    nodes = nodes.loc[nodes['user_id'] == user_id]
    sections = pd.read_sql('sections', engine)
    sections = sections.loc[sections['user_id'] == user_id]
    point_loads = pd.read_sql('point_loads', engine)
    point_loads = point_loads.loc[point_loads['user_id'] == user_id]
    dist_loads = pd.read_sql('loads_nodal', engine)
    dist_loads = dist_loads.loc[dist_loads['user_id'] == user_id]

    elements.to_csv('elements.csv')
    truss_elements.to_csv('truss_elements.csv')
    nodes.to_csv('nodes')
    sections.to_csv('sections.csv')

    return elements, nodes, sections, point_loads, dist_loads, truss_elements


# calculate DOFS
def dofs(nodes):
    t1 = time.time()
    nodes_n = len(nodes)
    #   #get 1D array of the constraints
    constraints = nodes.iloc[:, [6, 7, 8, 9, 10, 11]].get_values().flatten(order='C')
    #   #argsort returns the indexes to sort the constraints to free and sup
    dofs = constraints.argsort()
    node_dofs = pd.DataFrame(np.reshape(np.sort(dofs), (nodes_n, 6)))
    node_dofs['nn'] = nodes['nn']
    node_dofs.columns = ['dofx', 'dofy', 'dofz', 'dofrx', 'dofry', 'dofrz', 'nn']
    a = constraints[constraints.argsort()]
    temp = np.where(a == 0)
    slice = temp[0][len(temp[0]) - 1] + 1
    sup_dofs = sorted(dofs[:slice].tolist())
    free_dofs = sorted(dofs[slice:].tolist())
    arranged_dofs = free_dofs + sup_dofs
    print('DOFS: ', time.time() - t1)
    return arranged_dofs, free_dofs, sup_dofs, node_dofs


def stifness_array(dofs, elements, nodes, sections, node_dofs, truss_elements, point_loads):
    t1 = time.time()
    local_stifness = []
    transf_arrays = []
    step = len(nodes) * 6
    K_ol = np.zeros((step, step))
    for index, elm in elements.iterrows():
        nodei = nodes.loc[nodes.nn == elm.nodei]
        nodej = nodes.loc[nodes.nn == elm.nodej]
        sect = sections.loc[sections.section_id == elm.section_id]
        k = local_stif(elm, sect)
        local_stifness.append(k.copy())
        rot = transformation_array(elm, nodei, nodej, point_loads)
        transf_arrays.append(rot.copy())
        t = np.transpose(rot).dot(k).dot(rot)
        i = nodei.nn.get_values()[0]
        j = nodej.nn.get_values()[0]
        if elm.elem_type == 'beam':
            dofs_i = node_dofs.loc[node_dofs.nn == i]
            dofs_j = node_dofs.loc[node_dofs.nn == j]
            dof_a, dof_b = dofs_i['dofx'].get_values()[0], \
                           dofs_i['dofrz'].get_values()[0] + 1
            dof_c, dof_d = dofs_j['dofx'].get_values()[0], \
                           dofs_j['dofrz'].get_values()[0] + 1
            K_ol[dof_a:dof_b, dof_a:dof_b] += t[:6, :6]
            K_ol[dof_a:dof_b, dof_c:dof_d] += t[:6, 6:]
            K_ol[dof_c:dof_d, dof_a:dof_b] += t[6:, :6]
            K_ol[dof_c:dof_d, dof_c:dof_d] += t[6:, 6:]
        else:
            dof_a, dof_b = node_dofs.loc[node_dofs.nn == nodei.nn]['dofx'].get_values()[0], \
                           node_dofs.loc[node_dofs.nn == nodei.nn]['dofz'].get_values()[0] + 1
            dof_c, dof_d = node_dofs.loc[node_dofs.nn == nodej.nn]['dofx'].get_values()[0], \
                           node_dofs.loc[node_dofs.nn == nodej.nn]['dofz'].get_values()[0] + 1
            K_ol[dof_a:dof_b, dof_a:dof_b] += t[:3, :3]
            K_ol[dof_a:dof_b, dof_c:dof_d] += t[:3, 3:]
            K_ol[dof_c:dof_d, dof_a:dof_b] += t[3:, :3]
            K_ol[dof_c:dof_d, dof_c:dof_d] += t[3:, 3:]

    i_uper = np.triu_indices(step, 0)

    K_ol[i_uper] = K_ol.T[i_uper]
    print('arrays: ', time.time() - t1)
    return local_stifness, transf_arrays, K_ol


def local_stif(element, sect):
    L = element.length
    elem_type = element.elem_type

    # A, E = sect.A, sect.E
    A = 0.2090318
    E = 199948023.75
    if elem_type == 'beam':
        # Iy, Iz, G, J = sect.Ix, sect.Iy, sect.G, sect.Iz
        Iy = 0.00364
        Iz = 0.00364
        G = 76904146.79
        J = 0.00614
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
        precision = 3
        y[0, 0] = w1
        y[6, 0] = -w1
        y[1, 1] = w2
        y[5, 1] = w3
        y[7, 1] = -w2
        y[11, 1] = w3
        y[2, 2] = w6
        y[4, 2] = -w7
        y[8, 2] = -w6
        y[10, 2] = -w7
        y[3, 3] = w10
        y[9, 3] = -w10
        y[4, 4] = w8
        y[8, 4] = w7
        y[10, 4] = w9
        y[5, 5] = w4
        y[11, 5] = w5
        y[6, 6] = w1
        y[7, 5] = w7
        y[7, 7] = w2
        y[11, 7] = -w3
        y[8, 8] = w6
        y[10, 8] = w7
        y[9, 9] = w10
        y[10, 10] = w8
        y[11, 11] = w4

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

        # y = np.round(y, precision)

    else:
        w1 = E * A / L
        y = np.array([[w1, 0, 0, -w1, 0, 0],
                      [0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0],
                      [-w1, 0, 0, w1, 0, 0],
                      [0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0]])

    return y


def transformation_array(element, nodei, nodej, point_loads):
    L = element.length
    i, j = element.nodei, element.nodej

    x1, x2 = nodei.coord_x.get_values()[0], nodej.coord_x.get_values()[0]
    y1, y2 = nodei.coord_y.get_values()[0], nodej.coord_y.get_values()[0]
    z1, z2 = nodei.coord_z.get_values()[0], nodej.coord_z.get_values()[0]
    # need to find what works for the random case

    #
    # transform the loads here, its easier
    p_load = point_loads.loc[(point_loads.nn == element.en) & (point_loads.c!=99999)]

    CXx = (x2 - x1) / L
    CYx = (y2 - y1) / L
    CZx = (z2 - z1) / L

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

            Lambda[2, 0] = -COSY
            Lambda[2, 1] = 0
            Lambda[2, 2] = SINY
            Lambda[1, 0] = SINY
            Lambda[1, 1] = 0
            Lambda[1, 2] = COSY
            if y1 >= y2:
                Lambda[1, 0] = COSY
                Lambda[2, 0] = -SINY
        else:
            Lambda[2, 0] = -(CXx * CYx * COSY + CZx * SINY) / SQ
            Lambda[2, 1] = SQ * COSY
            Lambda[2, 2] = (-CYx * CZx * COSY + CXx * SINY) / SQ
            Lambda[1, 0] = (CXx * CYx * SINY - CZx * COSY) / SQ
            Lambda[1, 1] = -SQ * SINY
            Lambda[1, 2] = (CYx * CZx * SINY + CXx * COSY) / SQ

    LAMDA = np.zeros((12, 12))
    zeroes = np.array([0, 0, 0])
    LAMDA[:3, :3], LAMDA[3:6, 3:6] = Lambda, Lambda
    LAMDA[6:9, 6:9], LAMDA[9:, 9:] = Lambda, Lambda
    return LAMDA


def nodal_forces(point_loads, elem_loads, node_dofs, tranf_arrays, arranged_dofs, elements):
    P_nodal = np.zeros((len(arranged_dofs), 1))
    # diaforopoiisi gia truss elements
    for index, load in point_loads.iterrows():
        if load.c == 99999:
            node = load.nn
            a, b = node_dofs.loc[node_dofs.nn == node]['dofx'].get_values()[0], \
                   node_dofs.loc[node_dofs.nn == node]['dofrz'].get_values()[0] + 1
            P_nodal[a:b] += [[load.p_x], [load.p_y], [load.p_z],
                            [load.m_x], [load.m_y], [load.m_z]]
        else:
            elm_id = load.nn
            elm = elements.loc[elements.en == elm_id]
            L = elm.length.get_values()[0]
            nodei = elm.nodei.get_values()[0]
            nodej = elm.nodej.get_values()[0]
            dofa, dofb = node_dofs.loc[node_dofs.nn == nodei]['dofx'].get_values()[0], \
                   node_dofs.loc[node_dofs.nn == nodei]['dofrz'].get_values()[0] + 1
            dofc, dofd = node_dofs.loc[node_dofs.nn == nodej]['dofx'].get_values()[0], \
                   node_dofs.loc[node_dofs.nn == nodej]['dofrz'].get_values()[0] + 1
            a = load.c*L
            b = (1-load.c)*L

            p = load.iloc[[4,5,6,7,8,9]].get_values()
            A_i = np.zeros((6,1))
            A_j = np.zeros((6, 1))
            A_i[0] = -p[0]*(1-load.c)
            A_j[0] = p[0]*load.c
            A_i[1] = -p[1] * (a / L - a ** 2 * b / L ** 3 + a * b ** 2 / L ** 3)
            A_j[1] = p[1] * (a / L + a ** 2 * b / L ** 3 - a * b ** 2 / L ** 3)
            A_i[2] = -p[2] * (a / L - a ** 2 * b / L ** 3 + a * b ** 2 / L ** 3)
            A_j[2] = p[2] * (a / L + a ** 2 * b / L ** 3 - a * b ** 2 / L ** 3)
            A_i[3] = p[3]*(1-load.c)
            A_j[3] = p[3]*load.c
            A_i[4] = p[2] * a * b ** 2/L**2
            A_j[4] = p[2] * a ** 2 * b/L**2
            A_i[5] = -p[1] * a * b ** 2/L**2
            A_j[5] = -p[1] * a ** 2 * b / L ** 2

            # element forces from to local to global
            rot = tranf_arrays[elm.index[0]][:6, :6]
            P_nodal[dofa:dofb] += rot.dot(A_i)
            P_nodal[dofc:dofd] += rot.dot(A_j)

    return P_nodal


def solver(K, P_nodal, dofs, dofs_arranged, free):
    # rearagment of the arrays
    K_m = rearrangment(K, dofs_arranged)
    P_m = rearrangment(P_nodal, dofs_arranged)

    P_f = P_m[:free]

    Kff = K_m[:free, :free]
    Ksf = K_m[free:, :free]

    D_f = np.linalg.inv(Kff).dot(P_f)
    P_s = np.dot(Ksf, D_f)
    P_s = np.round(P_s, decimals=2)

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


def nodal_mqn(K, Lamda, displacments, elements, node_dofs, K_ol, nodes, point_loads):
    for index, elm in elements.iterrows():
        i = index

        sect = None
        nodei = nodes.loc[nodes.nn == elm.nodei]
        nodej = nodes.loc[nodes.nn == elm.nodej]
        k = local_stif(elm, sect)

        rot = transformation_array(elm, nodei, nodej, point_loads)

        nodei = elm.nodei
        nodej = elm.nodej
        k = local_stif(elm, sect)

        a, b = node_dofs.loc[node_dofs.nn == nodei]['dofx'].get_values()[0], \
               node_dofs.loc[node_dofs.nn == nodei]['dofrz'].get_values()[0] + 1
        c, d = node_dofs.loc[node_dofs.nn == nodej]['dofx'].get_values()[0], \
               node_dofs.loc[node_dofs.nn == nodej]['dofrz'].get_values()[0] + 1
        d_elem = np.zeros((12, 1))
        d_elem[:6], d_elem[6:] = displacments[a:b], displacments[c:d]
        # local displacments
        d_local = rot.dot(d_elem)
        MQN = k.dot(d_local)
        MQN = np.round(MQN, 2)

        return MQN


def rotate_loads(elements, point_loads, transf_arrays):
    for index, element in elements.iterrows():
        L = element.length



        # transform the loads here, its easier
        p_load = point_loads.loc[(point_loads.nn == element.en) & (point_loads.c != 99999)]
        if p_load.empty==False:
            #P_x = np.array([p_load.p_x.get_values()[0], 0, 0])
            #P_y = np.array([0, p_load.p_y.get_values()[0], 0])
            P_z = np.array([0, 0, p_load.p_z.get_values()[0]])

            rot = transf_arrays[index][:3, :3]
            #p = rot.dot(P_x) + rot.dot(P_y) +\
            p = rot.dot(P_z)

            # .p_x,  point_loads.iloc[p_load.index].p_y,  point_loads.iloc[p_load.index].p_z = p[0], p[1], p[2]
            p_load['p_x'], p_load['p_y'], p_load['p_z'] = p[0], p[1], p[2]
            point_loads.iloc[p_load.index, :] = p_load

    return point_loads

def mqn_member():
    pass


def main(user_id):
    elements, nodes, sections, point_loads, dist_loads, truss_elements = load_data(user_id)

    arranged_dofs, free_dofs, sup_dofs, node_dofs = dofs(nodes)

    local_stifness, transf_arrays, K_ol = stifness_array(dofs, elements, nodes, sections, node_dofs, truss_elements, point_loads)

    point_loads_tr = rotate_loads(elements, point_loads, transf_arrays)
    print(point_loads_tr.to_string())

    P_nodal = nodal_forces(point_loads, dist_loads, node_dofs, transf_arrays, arranged_dofs, elements)

    P_s, D = solver(K_ol, P_nodal, arranged_dofs, arranged_dofs, len(free_dofs))

    MQN = nodal_mqn(local_stifness, transf_arrays, D, elements, node_dofs, K_ol, nodes, point_loads)

    print(P_s)
    print(MQN)
    print(D)


t1 = time.time()
main('cv13116')
print('Run: ', time.time() - t1)
