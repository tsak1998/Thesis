from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, reconstructor

from functions_new import *
from collections import defaultdict
import numpy as np

from time import time

t1 = time()

engine = create_engine('mysql+pymysql://root:password@localhost/yellow')

Base = declarative_base()


class Nodes(Base):
    __tablename__ = 'nodes'
    __nodes__ = defaultdict(int)
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', String(45), nullable=False)
    nn = Column('number', Integer)
    x = Column('coord_x', Float)
    y = Column('coord_y', Float)
    z = Column('coord_z', Float)
    dof_dx = Column('dof_dx', Integer)
    dof_dy = Column('dof_dy', Integer)
    dof_dz = Column('dof_dz', Integer)
    dof_rx = Column('dof_rx', Integer)
    dof_ry = Column('dof_ry', Integer)
    dof_rz = Column('dof_rz', Integer)
    nodes_sum = Column('nodes_sum', Integer)
    nn_opt = Column('nn_opt', Integer)

    # dofs = [dof_dx, dof_dy, dof_dz, dof_rx, dof_ry, dof_rz]

    @reconstructor
    def __init__(self):
        self.__class__.__nodes__[self.nn] = self
        self.dofs = np.array([self.dof_dx, self.dof_dy, self.dof_dz, self.dof_rx, self.dof_ry, self.dof_rz], dtype=int)


class Elements(Base):
    __tablename__ = 'elements'
    __elements__ = defaultdict(int)
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', String(45), nullable=False)
    en = Column('number', Integer)
    ni = Column('nodei', Integer)
    nj = Column('nodej', Integer)
    length = Column('length', Float)
    section = Column('section_id', Integer)
    elem_type = Column('elem_type', String)
    fixity_dx_i = Column('fixity_dx_i', Integer)
    fixity_dy_i = Column('fixity_dy_i', Integer)
    fixity_dz_i = Column('fixity_dz_i', Integer)
    fixity_rx_i = Column('fixity_rx_i', Integer)
    fixity_ry_i = Column('fixity_ry_i', Integer)
    fixity_rz_i = Column('fixity_rz_i', Integer)
    fixity_dy_j = Column('fixity_dy_j', Integer)
    fixity_dx_j = Column('fixity_dx_j', Integer)
    fixity_dz_j = Column('fixity_dz_j', Integer)
    fixity_rx_j = Column('fixity_rx_j', Integer)
    fixity_ry_j = Column('fixity_ry_j', Integer)
    fixity_rz_j = Column('fixity_rz_j', Integer)
    en_opt = Column('en_opt', Integer)
    ni_opt = Column('ni_opt', Integer)
    nj_opt = Column('nj_opt', Integer)

    @reconstructor
    def __init__(self):
        self.__class__.__elements__[self.en] = self
        self.ni = Nodes.__nodes__[self.ni]
        self.nj = Nodes.__nodes__[self.nj]
        self.section = Sections.__sections__[self.section]
        L = self.length
        section = self.section
        material = section.material
        self.stifness_loc = local_stifness(L, material.E, material.G, section.A, section.Ix, section.Iy, section.Iz)
        self.transform = transformation_array(L, self.ni.x, self.ni.y, self.ni.z, self.nj.x, self.nj.y, self.nj.z, 0)
        self.stifness_glob = np.transpose(self.transform).dot(self.stifness_loc).dot(self.transform)


class Materials(Base):
    __tablename__ = 'materials'
    __materials__ = defaultdict(int)
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', String(45), nullable=False)
    material_id = Column('material_id', Integer)
    E = Column('E', Float)
    G = Column('G', Float)

    @reconstructor
    def __init__(self):
        self.__class__.__materials__[self.material_id] = self


class Sections(Base):
    __tablename__ = 'sections'
    __sections__ = defaultdict(int)
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', String(45), nullable=False)
    section_id = Column('section_id', Integer)
    material = Column('material', Integer)
    type = Column('type', String(10))
    dimensions = Column('dimensions', String(10))
    A = Column('A', Float)
    Ix = Column('Ix', Float)
    Iy = Column('Iy', Float)
    Iz = Column('Iz', Float)

    @reconstructor
    def __init__(self):
        self.__class__.__sections__[self.section_id] = self
        self.material = Materials.__materials__[self.material]


class PointLoads(Base):
    __tablename__ = 'point_loads'
    __pLoadsNode__ = defaultdict(int)
    __pLoadsElement__ = defaultdict(int)
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', String(45), nullable=False)
    nn = Column('number', Integer)
    c = Column('c', Float)
    p_x = Column('p_x', Float)
    p_y = Column('p_y', Float)
    p_z = Column('p_z', Float)
    m_x = Column('m_x', Float)
    m_y = Column('m_y', Float)
    m_z = Column('m_z', Float)

    @reconstructor
    def __init__(self):
        if self.c == 99999:
            self.__class__.__pLoadsNode__[self.nn] = self
        else:
            self.__class__.__pLoadsElement__[self.nn] = self


# create tables
Base.metadata.create_all(bind=engine)

# create session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
