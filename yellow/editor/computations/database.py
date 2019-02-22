from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://bucketuser:dencopc@localhost/bucketlist')
db_session = scoped_session(sessionmaker(autocommit = False,
										autoflush = False,
										bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
	from tables import nodes, elements, loads_nodal, loads_element, sections
	Base.metadata.create_all(bind=engine)
