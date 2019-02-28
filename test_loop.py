import numpy as np
import math
import pandas as pd
from sqlalchemy import create_engine
from scipy.sparse import csr_matrix
import time


def load_data(user_id):
    engine = create_engine("mysql+pymysql://root:password@localhost:3306/_0000125")
    elements = pd.read_sql('elements', engine)
    elements = elements.loc[elements['user_id'] == user_id]
    truss_elements = elements.loc[elements['elem_type'] == 'truss']
    nodes = pd.read_sql('nodes', engine)
    nodes = nodes.loc[nodes['user_id'] == user_id]
    sections = pd.read_sql('sections', engine)
    sections = sections.loc[sections['user_id'] == user_id]
    point_loads = pd.read_sql('loads_nodal', engine)
    point_loads = point_loads.loc[point_loads['user_id'] == user_id]
    dist_loads = pd.read_sql('loads_nodal', engine)
    dist_loads = dist_loads.loc[dist_loads['user_id'] == user_id]

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


def stifness_array(dofs, elements, nodes, sections, node_dofs, truss_elements):
    t1 = time.time()
    local_stifness = []
    transf_arrays = []

    step = len(nodes) * 6
    K_ol = np.zeros((step, step))

    for i in range(len(elements)):
        # maybe separate functions for truss and beams so it will do the ifs once per loop
        elm = elements.iloc[i]
        nodei = nodes.loc[nodes.nn == elm.nodei]
        nodej = nodes.loc[nodes.nn == elm.nodej]
        sect = sections.loc[sections.section_id == elm.section_id]
        k = local_stif(elm, sect)
        rot = transformation_array(elm, nodei, nodej)
        local_stifness.append(k)
        transf_arrays.append(rot)
        if elm.elem_type == 'beam':
            t = np.transpose(rot).dot(k).dot(rot)
            dof_a, dof_b = node_dofs.loc[node_dofs.nn == nodei]['dofx'].get_values()[0], \
                           node_dofs.loc[node_dofs.nn == nodei]['dofz'].get_values()[0] + 1
            dof_c, dof_d = node_dofs.loc[node_dofs.nn == nodej]['dofx'].get_values()[0], \
                           node_dofs.loc[node_dofs.nn == nodej]['dofz'].get_values()[0] + 1
            K_ol[dof_a:dof_b, dof_a:dof_b] += t[:6, :6]
            K_ol[dof_a:dof_b, dof_c:dof_d] += t[:6, 6:]
            K_ol[dof_c:dof_d, dof_a:dof_b] += t[6:, :6]
            K_ol[dof_c:dof_d, dof_c:dof_d] += t[6:, 6:]
        else:
            t = np.transpose(rot).dot(k).dot(rot)
            dof_a, dof_b = node_dofs.loc[node_dofs.nn == nodei]['dofx'].get_values()[0], \
                           node_dofs.loc[node_dofs.nn == nodei]['dofz'].get_values()[0] + 1
            dof_c, dof_d = node_dofs.loc[node_dofs.nn == nodej]['dofx'].get_values()[0], \
                           node_dofs.loc[node_dofs.nn == nodej]['dofz'].get_values()[0] + 1
            K_ol[dof_a:dof_b, dof_a:dof_b] += k[:3, :3]
            K_ol[dof_a:dof_b, dof_c:dof_d] += k[:3, 3:]
            K_ol[dof_c:dof_d, dof_a:dof_b] += k[3:, :3]
            K_ol[dof_c:dof_d, dof_c:dof_d] += k[3:, 3:]




    print('arrays: ', time.time() - t1)
    return local_stifness, transf_arrays, K_ol


'''
if (r.elem_type == 'beam'):
    a, b, c, d = int(dofs[i, 1]) - 1, int(dofs[i, 6]), int(dofs[i, 7]) - 1, int(dofs[i, 12])
    K_ol[a:b, a:b] += k[:6, :6]
    K_ol[a:b, c:d] += k[:6, 6:]
    K_ol[c:d, a:b] += k[6:, :6]
    K_ol[c:d, c:d] += k[6:, 6:]
else:
    a, b, c, d = int(dofs[i, 1]) - 1, int(dofs[i, 3]), int(dofs[i, 7]) - 1, int(dofs[i, 9])
    K_ol[a:b, a:b] += k[:3, :3]
    K_ol[a:b, c:d] += k[:3, 3:]
    K_ol[c:d, a:b] += k[3:, :3]
    K_ol[c:d, c:d] += k[3:, 3:]
'''


def local_stif(element, sect):
    L = element.length
    elem_type = element.elem_type

    A, E = sect.A, sect.E
    if elem_type == 'beam':
        Iy, Iz, G, J = sect.Ix, sect.Iy, sect.G, sect.Iz
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
        y[1, 0] = w2
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
        y[7, 7] = w2
        y[11, 7] = -w3
        y[8, 8] = w6
        y[10, 8] = w7
        y[9, 9] = w10
        y[10, 10] = w8
        y[11, 11] = w4

        y = np.round(y, precision)


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

    x1, x2 = nodei.coord_x.get_values(), nodej.coord_x.get_values()
    y1, y2 = nodei.coord_y.get_values(), nodej.coord_y.get_values()
    z1, z2 = nodei.coord_z.get_values(), nodej.coord_z.get_values()

    xR, yR, zR = 0, 1, 0

    cx = (x2 - x1) / L
    cy = (y2 - y1) / L
    cz = (z2 - z1) / L
    Lambda = np.zeros((3, 3))
    if element.elem_type == 'beam':
        if math.sqrt(cx ** 2 + cz ** 2) != 0:
            Lambda[0, 0] = cx
            Lambda[0, 1] = cy
            Lambda[0, 2] = cz
            Lambda[1, 0] = (-cx * cy) / math.sqrt(cx ** 2 + cz ** 2)
            Lambda[1, 1] = math.sqrt(cx ** 2 + cz ** 2)
            Lambda[1, 2] = (-cy * cz) / math.sqrt(cx ** 2 + cz ** 2)
            Lambda[2, 0] = (-cz) / math.sqrt(cx ** 2 + cz ** 2)
            Lambda[2, 1] = 0
            Lambda[2, 2] = cx / math.sqrt(cx ** 2 + cz ** 2)
        else:
            Lambda[0, 0] = 0
            Lambda[0, 1] = cy
            Lambda[0, 2] = 0
            Lambda[1, 0] = -cy
            Lambda[1, 1] = 0
            Lambda[1, 2] = 0
            Lambda[2, 0] = 0
            Lambda[2, 1] = 0
            Lambda[2, 2] = 1

        LAMDA = np.zeros((12, 12))
        zeroes = np.array([0, 0, 0])

        LAMDA[:3, :3], LAMDA[3:6, 3:6] = Lambda, Lambda
        LAMDA[6:9, 6:9], LAMDA[9:, 9:] = Lambda, Lambda
    else:
        dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
        cosx, cosy, cosz = dx / L, dy / L, dz / L

        LAMDA = np.array([[cosx, cosy, cosz, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0],
                          [0, 0, 0, cosx, cosy, cosz],
                          [0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0]])

    return LAMDA


def main(user_id):
    elements, nodes, sections, point_loads, dist_loads, truss_elements = load_data(user_id)
    arranged_dofs, free_dofs, sup_dofs, node_dofs = dofs(nodes)
    local_stifness, transf_arrays, K_ol = stifness_array(dofs, elements, nodes, sections, node_dofs, truss_elements)


t_ol = time.time()
main('cv13116')
print('Run: ', time.time() - t_ol)
