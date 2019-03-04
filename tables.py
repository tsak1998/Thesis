from sqlalchemy import Column, Integer, String, Float
from database import Base


#nodes table
class nodes(Base):
	__tablename__ = 'nodes'
	id = Column('id', Integer, primary_key=True)
	user_id =  Column('user_id', String(45), nullable = False)
	nn = Column('nn', Integer)
	coord_x = Column('coord_x', Float)
	coord_y = Column('coord_y', Float)
	coord_z = Column('coord_z', Float)
	dof_dx = Column('dof_dx', Integer)
	dof_dy = Column('dof_dy', Integer)
	dof_dz = Column('dof_dz', Integer)
	dof_rx = Column('dof_rx', Integer)
	dof_ry = Column('dof_ry', Integer)
	dof_rz = Column('dof_rz', Integer)
	
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

#elements table
class elements(Base):
	__tablename__ = 'elements'
	id = Column('id', Integer, primary_key=True)
	user_id =  Column('user_id', String(45), nullable = False)
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
		
#loads tables
class point_loads(Base):
	__tablename__ = 'point_loads'
	id = Column('id', Integer, primary_key=True)
	user_id =  Column('user_id', String(45), nullable = False)
	nn = Column('nn', Integer)
	c = Column('c', Float)
	p_x = Column('p_x', Float)
	p_y = Column('p_y', Float)
	p_z = Column('p_z', Float)
	m_x = Column('m_x', Float)
	m_y = Column('m_y', Float)
	m_z = Column('m_z', Float)
	
	def __init__(self, user_id, nn, c, p_x, p_y, p_z, m_x, m_y, m_z):  # constructor
		self.user_id = user_id
		self.nn = nn
		self.c = c
		self.p_x = p_x
		self.p_y = p_y
		self.p_z = p_z
		self.m_x = m_x
		self.m_y = m_y
		self.m_z = m_z


class loads_element(Base):
	__tablename__ = 'loads_element'
	id = Column('id', Integer, primary_key=True)
	user_id =  Column('user_id', String(45), nullable = False)
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
	user_id =  Column('user_id', String(45), nullable = False)
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
		self.E =  E
		self.G = G
		self.A = A
		self.Ix = Ix
		self.Iy = Iy
		self.Iz = Iz

