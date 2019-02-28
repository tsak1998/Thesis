import numpy as np
import math
import copy
import sys, os, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
import time

engine = create_engine("mysql+pymysql://root:password@localhost:3306/_0000125")
#engine = create_engine("mysql+pymysql://bucketuser:dencopc@localhost:3306/bucketlist")
db_session = scoped_session(sessionmaker(autocommit = False,
										autoflush = False,
										bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
	from tables import nodes, elements, loads_nodal, loads_element, sections
	Base.metadata.create_all(bind=engine)


# nodes table
class nodes(Base):
	__tablename__ = 'nodes'
	id = Column('id', Integer, primary_key=True)
	user_id = Column('user_id', String(45), nullable=False)
	nn = Column('nn', Integer)
	coord_x = Column('coord_x', Float)
	coord_y = Column('coord_y', Float)
	coord_z = Column('coord_z', Float)
	dof_dx = Column('dof_dx', String(5))
	dof_dy = Column('dof_dy', String(5))
	dof_dz = Column('dof_dz', String(5))
	dof_rx = Column('dof_rx', String(5))
	dof_ry = Column('dof_ry', String(5))
	dof_rz = Column('dof_rz', String(5))

	def __init__(self, user_id, nn, coord_x, coord_y, coord_z,
				 dof_dx, dof_dy, dof_dz,
				 dof_rx, dof_ry, dof_rz):  # constructor
		self.user_id = user_id
		self.nn = nn
		self.coord_x = coord_x
		self.coord_y = coord_y
		self.coord_z = coord_z
		self.dof_dx = dof_dx
		self.dof_dy = dof_dy
		self.dof_dz = dof_dz
		self.dof_rx = dof_rx
		self.dof_ry = dof_ry
		self.dof_rz = dof_rz


# elements table
class elements(Base):
	__tablename__ = 'elements'
	id = Column('id', Integer, primary_key=True)
	user_id = Column('user_id', String(45), nullable=False)
	en = Column('en', Integer)
	nodei = Column('nodei', Float)
	nodej = Column('nodej', Float)
	length = Column('length', Float)
	elem_type = Column('elem_type', String(5))
	section_id = Column('section_id', Integer)

	def __init__(self, user_id, en, nodei, nodej, length, elem_type, section_id):  # constructor
		self.user_id = user_id
		self.en = en
		self.nodei = nodei
		self.nodej = nodej
		self.length = length
		self.elem_type = elem_type
		self.section_id = section_id


# loads tables
class loads_nodal(Base):
	__tablename__ = 'loads_nodal'
	id = Column('id', Integer, primary_key=True)
	user_id = Column('user_id', String(45), nullable=False)
	nn = Column('nn', Integer)
	p_x = Column('p_x', Float)
	p_y = Column('p_y', Float)
	p_z = Column('p_z', Float)
	m_x = Column('m_x', Float)
	m_y = Column('m_y', Float)
	m_z = Column('m_z', Float)

	def __init__(self, user_id, nn, p_x, p_y, p_z, m_x, m_y, m_z):  # constructor
		self.user_id = user_id
		self.nn = nn
		self.p_x = p_x
		self.p_y = p_y
		self.p_z = p_z
		self.m_x = m_x
		self.m_y = m_y
		self.m_z = m_z


class loads_element(Base):
	__tablename__ = 'loads_element'
	id = Column('id', Integer, primary_key=True)
	user_id = Column('user_id', String(45), nullable=False)
	en = Column('en', Integer)
	p1 = Column('p1', Float)
	p2 = Column('p2', Float)
	a = Column('a', Float)
	c = Column('c', Float)
	l = Column('l', Float)

	def __init__(self, user_id, en, p1, p2):  # constructor
		self.user_id = user_id
		self.nn = en
		self.p1 = p1
		self.p2 = p2


class sections(Base):
	__tablename__ = 'sections'
	id = Column('id', Integer, primary_key=True)
	user_id = Column('user_id', String(45), nullable=False)
	section_id = Column('section_id', Integer)
	E = Column('E', Float)
	G = Column('G', Float)
	A = Column('A', Float)
	Ix = Column('Ix', Float)
	Iy = Column('Iy', Float)
	Iz = Column('Iz', Float)

	def __init__(self, user_id, section_id, E, G, A, Ix, Iy, Iz):  # constructor
		self.user_id = user_id
		self.section_id = section_id
		self.E = E
		self.G = G
		self.A = A
		self.Ix = Ix
		self.Iy = Iy
		self.Iz = Iz

def load_data():
	element_data = elements.query.all()
	nodes_data = nodes.query.all()
	sections_data = sections.query.all()
	node_loads = loads_nodal.query.all()
	elem_loads = loads_element.query.all()
	truss_elements = elements.query.filter_by(elem_type='truss').all()
	truss_nodes = []
	for r in truss_elements:
		a = r.nodei

		b = r.nodej
		check1 = elements.query.filter_by(nodei=a, elem_type='beam').all() + elements.query.filter_by(nodej=a, elem_type='beam').all()

		check2 = elements.query.filter_by(nodej=b, elem_type='beam').all() + elements.query.filter_by(nodei=b, elem_type='beam').all()
		if len(check1)==0:
			truss_nodes.append(a)
		if len(check2)==0:
			truss_nodes.append(b)

	truss_nodes = sorted(list(set(truss_nodes)))

	return element_data, nodes_data, sections_data, node_loads, elem_loads, truss_nodes


import numpy as np
import math
import copy
import sys, os, inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


def length(coord):
	coord = np.asarray(coord)

	l = math.sqrt(sum((coord[0, :] - coord[1, :]) ** 2))

	return l


##degress of freedom ordering##
def dofs(nodes, elements, truss_nodes):
	step = len(nodes)
	count = 0
	dof_free = []
	dof_sup = []
	truss_nodes = np.array([truss_nodes])
	for r in nodes:
		constraints = [r.dof_dx, r.dof_dy, r.dof_dz, r.dof_rx, r.dof_ry, r.dof_rz]
		check = np.array([r.nn])
		if np.any(check == truss_nodes) == False:

			for j in range(6):
				dof = j + count
				if (int(constraints[j]) == 1):
					dof_free.append(dof)
				else:
					dof_sup.append(dof)
			count += 6
		else:
			for j in range(3):
				dof = j + count
				if (int(constraints[j]) == 1):
					dof_free.append(dof)
				else:
					dof_sup.append(dof)
			count += 3

	dofs_arranged = dof_free + dof_sup
	dofs_all = sorted(dofs_arranged)
	free = len(dof_free)
	sup = len(dof_sup)

	step = len(elements)
	step1 = len(nodes)

	dofs_array = np.zeros((step1, 7))
	dofs_array[0, 0] = nodes[0].nn
	dofs_array[0, 1:] = 1, 2, 3, 4, 5, 6
	dofs_element = np.zeros((step, 13))

	i = 1
	for r in nodes[1:]:
		check = np.array([r.nn])
		if any(check == truss_nodes) == False:
			dofs_array[i, 0] = r.nn
			dofs_array[i, 1:] = dofs_array[i - 1, 1:] + 6
		else:
			dofs_array[i, 0] = r.nn
			dofs_array[i, 4:] = 0, 0, 0
			if (dofs_array[i - 1, 4:] != 0, 0, 0):
				dofs_array[i, 1:4] = dofs_array[i - 1, 4:] + 3
			else:
				dofs_array[i, 1:4] = dofs_array[i - 1, 1:4] + 3
		i += 1

	i = 0
	for r in elements:
		dofs_element[i, 0] = r.en
		dofs_element[i, 1:7] = dofs_array[int(r.nodei) - 1, 1:]
		dofs_element[i, 7:] = dofs_array[int(r.nodej) - 1, 1:]
		i += 1

	dofs_element.astype(int)

	return dofs_all, dofs_arranged, free, dof_sup, dofs_element, dofs_array


def stif_array(dofs, elements, nodes, truss_nodes):
	# 6*(nodes-no_of_intersections)
	local_arrays = []
	transform_matrix = []
	step = 6 * len(nodes) - 3 * len(truss_nodes)
	# xreiazomai to array me ta nodes akris-telous
	K_ol = np.zeros((step, step))
	i = 0
	for r in elements:

		k = stifness(r)

		LAMDA = transform_array(r, nodes)
		local_arrays.append(k)
		transform_matrix.append(LAMDA)
		k = np.transpose(LAMDA).dot(k).dot(LAMDA)
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

		i += 1
	'''
	zero_rows = np.where(~K_ol.any(axis=0))[0]
	for r in zero_rows:
		K_ol[r, r] = 100
'''

	return K_ol, local_arrays, transform_matrix


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


def draseis_pagiwsis(dofs, loads, elem_loads, nodes_dofs, dofs_element, transform):
	P_nodal = np.zeros((len(dofs), 1))
	# diaforopoiisi gia truss elements
	for r in loads:
		a, b = int(nodes_dofs[r.nn - 1, 1]) - 1, int(nodes_dofs[r.nn - 1, 6])
		P_nodal[a:b] = [[r.p_x], [r.p_y], [r.p_z], [r.m_x], [r.m_y], [r.m_z]]

	# ypologismos drasewn pagiwsis01 = {ndarray} [[ 0.          0.          1.          0.          0.          0.\n   0.          0.          0.          0.          0.          0.        ]\n [-0.98058068  0.19611614  0.          0.          0.          0.\n   0.          0.          0.          0.          0.          0.        ]\n [-0.19611614 -0.98058068  0.          0.          0.          0.\n   0.          0.          0.          0.          0.          0.        ]\n [ 0.          0.          0.          0.          0.          1.\n   0.          0.          0.          0.          0.          0.        ]\n [ 0.          0.          0.         -0.98058068  0.19611614  0.\n   0.          0.          0.          0.          0.          0.        ]\n [ 0.          0.          0.         -0.19611614 -0.98058068  0.\n   0.          0.          0.          0.          0.          0.        ]\n [ 0.          0.          0.          0.          0.          0.\n   0.          0.          1.          0.          0.          0.        ]\n [ 0......View as Array
	'''
	for r in elem_loads:
		a, b = int(dofs_element[r.en-1,1])-1, int(dofs_element[r.en-1,6])
		c ,d = int(dofs_element[r.en-1,7])-1, int(dofs_element[r.en-1,12])
		if r.p1==r.p2:
			Ar = np.array([[0], [0], [r.p1*r.c/2], [0], [-r.p1*r.l**2/12], [0],
						   [0], [0], [-r.p1*r.c/2], [0], [r.p1*r.l**2/12], [0]])

			#Ar = np.transpose(transform[r.en-1]).dot(Ar)
			P_nodal[a:b] += Ar[:6]
			P_nodal[c:d] += Ar[6:]
			'''
	return P_nodal


def nodal_mqn(K, Lamda, displacments, elements, dofs):
	step = len(K)
	mqn_element = np.zeros((step, 13))

	for i in range(step):
		mqn_element[i, 0] = i + 1
		if (elements[i].elem_type == "beam"):
			a, b, c, d = int(dofs[i, 1]) - 1, int(dofs[i, 6]), int(dofs[i, 7]) - 1, int(dofs[i, 12])
			d_elem = np.zeros((12, 1))
			d_elem[:6], d_elem[6:] = displacments[a:b], displacments[c:d]
			mqn_element[i, 1:] = np.reshape(K[i].dot(np.dot(Lamda[i], d_elem)), (1, 12))
		else:
			d_elem = np.zeros((6, 1))
			a, b, c, d = int(dofs[i, 1]) - 1, int(dofs[i, 3]), int(dofs[i, 7]) - 1, int(dofs[i, 9])
			d_elem[:3], d_elem[3:] = displacments[a:b], displacments[c:d]

			mqn_element[i, 1:7] = np.reshape(K[i].dot(np.dot(Lamda[i], d_elem)), (1, 6))
			mqn_element[i, 6:9] = copy.copy(mqn_element[i, 3:6])
			mqn_element[i, 3:6] = [0, 0, 0]

	return mqn_element


def solver(K, P_nodal, dofs, dofs_arranged, free):
	# rearagment of the arrays
	K_m = rearrangment(K, dofs_arranged)
	P_m = rearrangment(P_nodal, dofs_arranged)

	P_f = P_m[:free]

	# provlima gia 2d vgazei 0 seira/stili
	# eite vazoume arithmo sta midenika tis diagwniou
	# eite to vazoume sta supported wste na min einai sto Kff

	Kff = K_m[:free, :free]
	Ksf = K_m[free:, :free]

	# akraies antidraseis
	# L = np.linalg.cholesky(Kff)
	# L_ = np.conjugate(L)
	##D_f = a.dot(P_f)
	# D_f = np.linalg.inv(Kff).dot(P_f)
	D_f = np.linalg.solve(Kff, P_f)
	P_s = np.dot(Ksf, D_f)
	# P_s = Ksf.dot(D_f)  #+Kss.dot(D_s)
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


def transform_array(element, nodes):
	L = element.length
	i, j = int(element.nodei), int(element.nodej)

	x1, x2 = nodes[i - 1].coord_x, nodes[j - 1].coord_x
	y1, y2 = nodes[i - 1].coord_y, nodes[j - 1].coord_y
	z1, z2 = nodes[i - 1].coord_z, nodes[j - 1].coord_z

	xR, yR, zR = 0, 1, 0

	cx = (x2 - x1) / L
	cy = (y2 - y1) / L
	cz = (z2 - z1) / L
	Lambda = np.zeros((3, 3))
	if element.elem_type == 'beam':
		if (math.sqrt(cx ** 2 + cz ** 2) != 0):
			Lambda[0, 0] = cx
			Lambda[0, 1] = cy
			Lambda[0, 2] = cz
			Lambda[1, 0] = (-cx * cy) / math.sqrt(cx ** 2 + cz ** 2)
			Lambda[1, 1] = math.sqrt(cx ** 2 + cz ** 2)
			Lambda[1, 2] = (-cy * cz) / math.sqrt(cx ** 2 + cz ** 2)
			Lambda[2, 0] = (-cz) / math.sqrt(cx ** 2 + cz ** 2)
			Lambda[2, 1] = 0
			Lambda[2, 2] = (cx) / math.sqrt(cx ** 2 + cz ** 2)
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


# import DOFs, global_stifness, analysis, nodal_forces, nodal_reactions


# the connector loads needed data
element_data, nodes_data, sections_data, node_loads, elem_loads, truss_nodes = load_data()

dofs_all, dofs_arranged, free, dof_sup, dofs_element, nodes_dofs = dofs(nodes_data, element_data, truss_nodes)

K_ol, local_arrays, transformation_arrays = stif_array(dofs_element, element_data, nodes_data, truss_nodes)

P_nodal = draseis_pagiwsis(dofs_all, node_loads, elem_loads, nodes_dofs, dofs_element, transformation_arrays)

reactions, displacments = solver(K_ol, P_nodal, dofs_all, dofs_arranged, free)

mqn_element = nodal_mqn(local_arrays, transformation_arrays, displacments, element_data, dofs_element)
mqn_element = np.round(mqn_element, decimals=2)

print(reactions)
#print(P_nodal)