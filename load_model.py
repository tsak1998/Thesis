from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, reconstructor

engine = create_engine('mysql+pymysql://root:password@localhost/yellow')

Base = declarative_base()

class Nodes(Base):
    __tablename__ = 'nodes'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', String(45), nullable=False)
    number = Column('number', Integer)
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
    #dofs = [dof_dx, dof_dy, dof_dz, dof_rx, dof_ry, dof_rz]

    @reconstructor
    def __init__(self):
        self.dofs = [self.dof_dx, self.dof_dy, self.dof_dz, self.dof_rx, self.dof_ry, self.dof_rz]


    def __dofs_numbered__(self):
        tmp = self.__class__.nodes_N * 6 - 6
        self.dofs_numbered = range(tmp, tmp + 6)

# create tables
Base.metadata.create_all(bind=engine)

# create session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

tmp = session.query(Nodes).all()
tmp[0].__init__()
Nodes.query.all()