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
	


class dist_loads(Base):
	__tablename__ = 'dist_loads'
	id = Column('id', Integer, primary_key=True)
	user_id =  Column('user_id', String(45), nullable = False)
	en = Column('en', Integer)
	p_1_x = Column('p_1_x', Float)
	p_2_x = Column('p_2_x', Float)
	p_1_y = Column('p_1_y', Float)
	p_2_y = Column('p_2_y', Float)
	p_1_z = Column('p_1_z', Float)
	p_2_z = Column('p_2_z', Float)
	c = Column('c', Float)
	l = Column('l', Float)



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
	


