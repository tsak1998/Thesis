from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from app import db
from sqlalchemy import create_engine


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))


    def get_security_payload(self):
        return {
            'id': self.id,
            'name': self.username,
        }


    def __str__(self):
        return self.email


class Nodes(db.Model):
    __tablename__ = 'nodes'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', String(45), nullable=False)
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


class PointLoads(db.Model):
    __tablename__ = 'point_loads'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', String(45), nullable=False)
    nn = Column('nn', Integer)
    c = Column('c', Float)
    p_x = Column('p_x', Float)
    p_y = Column('p_y', Float)
    p_z = Column('p_z', Float)
    m_x = Column('m_x', Float)
    m_y = Column('m_y', Float)
    m_z = Column('m_z', Float)


class DistLoads(db.Model):
    __tablename__ = 'dist_loads'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', String(45), nullable=False)
    en = Column('en', Integer)
    p_1_x = Column('p_1_x', Float)
    p_2_x = Column('p_2_x', Float)
    p_1_y = Column('p_1_y', Float)
    p_2_y = Column('p_2_y', Float)
    p_1_z = Column('p_1_z', Float)
    p_2_z = Column('p_2_z', Float)
    c = Column('c', Float)
    l = Column('l', Float)


class Materials(db.Model):
    __tablename__ = 'materials'
    id = Column('id', Integer, primary_key=True)
    material = Column('material', String(10))
    material_category = Column('material_category', String(10))
    E = Column('E', Float)
    G = Column('G', Float)
    n = Column('n', Float)


class Sections(db.Model):
    __tablename__ = 'sections'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', String(45), nullable=False)
    section_id = Column('section_id', Integer)
    type = Column('type', String(10))
    E = Column('E', Float)
    G = Column('G', Float)
    A = Column('A', Float)
    Ix = Column('Ix', Float)
    Iy = Column('Iy', Float)
    Iz = Column('Iz', Float)


class steelSections(db.Model):
    __tablename__ = 'steel_sections'
    id = Column('id', Integer, primary_key=True)
    sect_type = Column('sect_type', String(10))
    A = Column('A', Float)
    Ix = Column('Ix', Float)
    Iy = Column('Iy', Float)
    Iz = Column('Iz', Float)


class Reactions(db.Model):
    __tablename__ = 'reactions'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', String(45), nullable=False)
    nn = Column('nn', Integer)
    Fx = Column('Fx', Float)
    Fy = Column('Fy', Float)
    Fz = Column('Fz', Float)
    Mx = Column('Mx', Float)
    My = Column('My', Float)
    Mz = Column('Mz', Float)


class Mqn(db.Model):
    __tablename__ = 'mqn'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', String(45), nullable=False)
    en = Column('en', Integer)
    Fx = Column('Fx', Float)
    Fy = Column('Fy', Float)
    Fz = Column('Fz', Float)
    Mx = Column('Mx', Float)
    My = Column('My', Float)
    Mz = Column('Mz', Float)


class Displacements(db.Model):
    __tablename__ = 'displacements'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', String(45), nullable=False)
    en = Column('en', Integer)
    ux = Column('ux', Float)
    uy = Column('uy', Float)
    uz = Column('uz', Float)


def create_table():
    Base = declarative_base()
    engine = create_engine('mysql+pymysql://root:pass@localhost/yellow')
    db.Model.metadata.create_all(bind=engine)

# create_table()
