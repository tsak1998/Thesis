import numpy as np
import math
import pandas as pd
from sqlalchemy import create_engine
import time


def load_data(user_id):
    engine = create_engine("mysql+pymysql://root:pass@localhost:3306/_0000125")
    elements = pd.read_sql('elements', engine)
    elements = elements.loc[elements['user_id']==user_id]
    truss_elements = elements.loc[elements['elem_type']=='truss']
    nodes = pd.read_sql('nodes', engine)
    nodes = nodes.loc[nodes['user_id']==user_id]
    sections = pd.read_sql('sections', engine)
    sections = sections.loc[sections['user_id']==user_id]
    point_loads = pd.read_sql('loads_nodal', engine)
    point_loads = point_loads.loc[point_loads['user_id'] == user_id]
    dist_loads = pd.read_sql('loads_nodal', engine)
    dist_loads = dist_loads.loc[dist_loads['user_id'] == user_id]

    return elements, nodes, sections, point_loads, dist_loads, truss_elements

#calculate DOFS
def dofs(nodes):
    nodes_n = len(nodes)
    #   #get 1D array of the constraints
    constraints = nodes.iloc[:,[6, 7, 8, 9, 10, 11]].get_values().flatten(order='C')
    #   #argsort returns the indexes to sort the constraints to free and sup

    dofs = constraints.argsort()
    node_dofs = np.reshape(np.sort(dofs), (nodes_n,6))
    a = constraints[constraints.argsort()]
    temp = np.where(a==0)
    slice = temp[0][len(temp[0])-1]+1
    free_dofs = sorted(dofs[:slice].tolist())
    sup_dofs = sorted(dofs[slice:].tolist())
    arranged_dofs = free_dofs+sup_dofs

    return arranged_dofs, free_dofs, sup_dofs

def stifness_array(elements, nodes, sections, truss_elements):
    local_K = []
    transformation_matrices = []



def stifness(element):

    h = 0.457
    b = 0.457
    L = element.length
    A = 0.2090318
    E = 199948023.75  ##23249128.83
    if element.elem_type == 'beam':

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

def main(user_id):
    elements, nodes, sections, point_loads, dist_loads, truss_elements = load_data(user_id)
    arranged_dofs, free_dofs, sup_dofs = dofs(nodes)

main('cv13116')