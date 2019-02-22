from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def create_tables(engine):
    db_session = scoped_session(sessionmaker(autocommit = False,
                                        autoflush = False,
                                        bind=engine))
    global Base
    Base = declarative_base()
    Base.query = db_session.query_property()
    from tables import nodes, elements
    Base.metadata.create_all(bind=engine)