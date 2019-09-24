import numpy as np
import pandas as pd
import math
from numba import jit
from collections import defaultdict
from sqlalchemy import create_engine

from time import time

t1 = time()


class Model:

    def __init__(self, nodes, elements, dofs, sections, materials, pLoads_nodal, pLoads_element, d_loads):
        self.nodes = nodes
        self.elements = elements
        self.dofs = dofs
        self.sections = sections
        self.materials = materials
        self.p_loads_nodal = pLoads_nodal
        self.p_loads_elem = pLoads_element
        self.d_loads = d_loads
        self.dofs = range(Node.nodes_N*6)
        # self.stifness =

    def __stifness__(self):
        elements = self.elements
        nodes_N = Node.nodes_N
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

        self.K_ol = K_ol

    def __orderDofs__(self):
        constraints = [d for key, value in self.nodes.items() for d in value.dofs]
        indices = __argsort__(constraints)
        tmp = [self.dofs[i] for i in indices]
        slic = constraints.count(0)
        self.supported_dofs = tmp[:slic]
        self.free_dofs = tmp[slic:]




'''
Defining the Node class
Each Node will be an instance of the class
array = number,x,y,z
nodes is a dictionary with keys the node number
'''


class Node:
    # a dictionary that holds all nodes(instance) with key the respective number
    nodes = defaultdict(int)
    nodes_N = 0

    def __init__(self, nn, x, y, z, dofs):
        self.number = nn
        self.x = x
        self.y = y
        self.z = z
        self.dofs = dofs
        # self.dofs_numbered = get the numbered dofs
        self.__class__.nodes[self.number] = self
        self.__class__.nodes_N += 1

    def __dofs_numbered__(self):
        tmp = self.__class__.nodes_N * 6 - 6
        self.dofs_numbered = range(tmp, tmp + 6)



    # get a specific node<aa
    @staticmethod
    def __node__(nn):
        return Node.nodes[nn]

    # get all the nodes
    @staticmethod
    def __nodes__():
        return Node.nodes



'''
Defining the Element class
Each ELement will be an instance of the class
array = ['number','node_i','node_j','section']
element is a dictionary with keys the element number
'''


class Element:
    # a dictionary that holds its element(instance) with key the respective number
    elements = defaultdict(int)

    def __init__(self, nn, ni, nj, sect, bt):
        self.number = nn
        self.node_i = Node.__node__(ni)
        self.node_j = Node.__node__(nj)
        self.section = Section.__section__(sect)
        self.beta = bt
        self.dofi_1 = self.node_i.dofs_numbered[0]
        self.dofi_2 = self.node_i.dofs_numbered[5] + 1
        self.dofj_1 = self.node_j.dofs_numbered[0]
        self.dofj_2 = self.node_j.dofs_numbered[5] + 1
        self.__class__.elements[self.number] = self

    def __length__(self):
        dx = self.node_i.x - self.node_j.x
        dy = self.node_i.y - self.node_j.y
        dz = self.node_i.z - self.node_j.z
        self.length = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

    def __stifness_loc__(self):
        L = self.length
        section = self.section
        material = section.material
        self.stifness_loc = local_stifness(L, material.E, material.G, section.A, section.Ix, section.Iy, section.Iz)

    def __stifness_glob__(self):
        self.stifness_glob = np.transpose(self.transform).dot(self.stifness_loc).dot(self.transform)

    def __transform__(self):
        L = self.length
        x1 = self.node_i.x
        y1 = self.node_i.y
        z1 = self.node_i.z
        x2 = self.node_j.x
        y2 = self.node_j.y
        z2 = self.node_j.z
        bt = self.beta
        self.transform = transformation_array(L, x1, y1, z1, x2, y2, z2, bt)

    def __startEndForces__(self):
        loads = pLoad.__pointLoad_el__(self.number)
        print(loads)


    # get a specific element
    @staticmethod
    def __element__(en):
        return Element.elements[en]

    # get all elements
    @staticmethod
    def __elements__():
        return Element.elements


'''
Defining the Section class
Each section will be an instance of the class
'number','material','A','Ix', Iy, Iz
sections is a dictionary with keys the element number
'''


class Section:
    # a dictionary that holds its section(instance) with key the respective number
    sections = defaultdict(int)

    def __init__(self, sn, mn, A, Ix, Iy, Iz):
        self.number = sn
        self.material = Material.__material__(mn)
        self.A = A
        self.Ix = Ix
        self.Iy = Iy
        self.Iz = Iz
        self.__class__.sections[self.number] = self

    @staticmethod
    def __section__(sect):
        return Section.sections[sect]

    @staticmethod
    def __sections__():
        return Section.sections

'''
Defining the Material class
Each material will be an instance of the class
'number','E','G'
materials is a dictionary with keys the element number
'''


class Material:
    # a dictionary that holds its ma(instance) with key the respective number
    materials = defaultdict(int)

    def __init__(self, number, E, G):
        self.number = number
        self.E = E
        self.G = G
        self.__class__.materials[self.number] = self

    @staticmethod
    def __material__(number):
        return Material.materials[number]

    @staticmethod
    def __materials__():
        return Material.materials




'''
Defining the Point Loads class
Each point load will be an instance of the class
is defined number, px, py, pz, mx, my, mz

PLoad for elements is a child of the pLoad class 
it has an extra attribute: c and en
'''


class pLoad:
    point_loads_node = defaultdict(list)
    point_loads_element = defaultdict(list)

    def __init__(self, px, py, pz, mx, my, mz):
        self.px = px
        self.py = py
        self.pz = pz
        self.mx = mx
        self.my = my
        self.mz = mz

    def __setNode__(self, nn):
        self.nn = Node.__node__(nn)

    def update_pLoads(self):
        self.__class__.point_loads_node[self.nn].append(self)

    @staticmethod
    def __pointLoad_el__(number):
        return pLoad.point_loads_element[number]

    @staticmethod
    def __pointLoad_els__():
        return pLoad.point_loads_element


    @staticmethod
    def __pointLoad_node__(number):
        return pLoad.point_loads_node[number]

    @staticmethod
    def __pointLoad_nodes__():
        return pLoad.point_loads_node


class pLoadsElement(pLoad):

    def __extend__(self, en, c):
        self.c = c
        self.en = en
        self.__class__.point_loads_element[self.en].append(self)


'''
Defining the Dist Loads class
Each point load will be an instance of the class
is defined number, c, px, py, pz, mx, my, mz
point_loads is a dictionary with keys the element number
'''


class Dist_Loads:
    dist_loads = defaultdict(int)

    def __init__(self, number, c, l, px1, px2, py1, py2, pz1, pz2):
        self.number = number
        self.c = c
        self.l = l
        self.px1 = px1
        self.px2 = px2
        self.py1 = py1
        self.py2 = py2
        self.pz1 = pz1
        self.pz2 = pz2
        self.__class__.dist_loads[self.number] = self

    @staticmethod
    def __distLoad__(number):
        return Dist_Loads.dist_loads[number]


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

def __argsort__(seq):
    return sorted(range(len(seq)), key=seq.__getitem__)

# def load_data(user_id, engine):
engine = create_engine('mysql+pymysql://root:password@localhost/yellow')
user_id = 'cv13116'

nodes = pd.read_sql("SELECT * from nodes WHERE user_id='" + user_id + "'", engine).sort_values(
    by=['number']).reset_index()
elements = pd.read_sql("SELECT * from elements WHERE user_id='" + user_id + "'", engine)
sections = pd.read_sql("SELECT * from sections WHERE user_id='" + user_id + "'", engine)
materials = pd.read_sql("SELECT * from materials WHERE user_id='" + user_id + "'", engine)
point_loads = pd.read_sql("SELECT * from point_loads WHERE user_id='" + user_id + "'", engine)
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
    temp_load.append((1, user_id, number, c, p_x, p_y, p_z, m_x, m_y, m_z))
    # df = pd.DataFrame([temp_load], columns=point_loads.columns)
point_loads_new = pd.DataFrame(temp_load, columns=point_loads.columns)

for index, node in nodes.iterrows():
    nn = node.number
    x = node.coord_x
    y = node.coord_y
    z = node.coord_z
    dofs = [node.dof_dx, node.dof_dy, node.dof_dz, node.dof_rx, node.dof_ry, node.dof_rz]
    tmp = Node(nn, x, y, z, dofs)
    tmp.__dofs_numbered__()

for index, material in materials.iterrows():
    mn = material.material_id
    E = material.E
    G = material.G
    Material(mn, E, G)

for index, section in sections.iterrows():
    sn = section.section_id
    mn = section.material
    A = section.A
    Ix = section.Ix
    Iy = section.Iy
    Iz = section.Iz
    Section(sn, mn, A, Ix, Iy, Iz)

for index, element in elements.iterrows():
    en = element.number
    ni = element.nodei
    nj = element.nodej
    sect = element.section_id
    bt = 0
    Element(en, ni, nj, sect, bt)
    tmp = Element.__element__(en)
    tmp.__length__()
    tmp.__stifness_loc__()
    tmp.__transform__()
    tmp.__stifness_glob__()
    tmp.__startEndForces__()

for index, p_load in point_loads.iterrows():
    if p_load.c == 99999:
        nn = p_load.number
        px = p_load.p_x
        py = p_load.p_y
        pz = p_load.p_z
        mx = p_load.m_x
        my = p_load.m_y
        mz = p_load.m_z
        tmp = pLoad(px, py, pz, mx, my, mz)
        tmp.__setNode__(p_load.number)
        tmp.update_pLoads()
    else:
        en = p_load.number
        c = p_load.c
        px = p_load.p_x
        py = p_load.p_y
        pz = p_load.p_z
        mx = p_load.m_x
        my = p_load.m_y
        mz = p_load.m_z
        tmp = pLoadsElement(px, py, pz, mx, my, mx)
        tmp.__extend__(en, c)

nodes_N = Node.nodes_N
dofs = range(nodes_N*6)
elements = Element.__elements__()
nodes = Node.__nodes__()
pLoads_nodal = pLoad.__pointLoad_nodes__()
pLoads_element = pLoad.__pointLoad_els__()
sections = Section.__sections__()
materials = Material.__materials__()
#dist_loads = Dist_Loads.__distLoads__()

#K = global_stifness(nodes_N, elements)
model = Model(nodes, elements, dofs, sections, materials, pLoads_nodal, pLoads_element, dist_loads)
model.__stifness__()
model.__orderDofs__()
print(time() - t1)

'''
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
    '''