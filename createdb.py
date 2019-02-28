import time
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database import create_tables


#creates the database
def init_db(projCode):
    
    #engine = create_engine("mysql+pymysql://bucketuser:dencopc@localhost:3306/bucketlist")
    try:
        engine = create_engine("mysql+pymysql://root:password@localhost:3306/"+projCode)
        engine.connect()

        #need to clear tables
    except:
        engine = create_engine("mysql+pymysql://root:password@localhost:3306/")
        engine.execute("CREATE DATABASE "+projCode) #create db
        engine.execute("USE "+projCode) # select new db
        #tables, the ones in table.py
        create_tables(engine)
    
    return engine


def createDB(projCode,**kwargs):
    time1 = time.time()
    #print(nod.head())
    #print(elm.head())
    proj_id = '_'
    l = len(str(projCode))
    print('lenght=',l)
    for x in range(7 - l):
        proj_id += '0'
    proj_id += str(projCode)

    engine = init_db(proj_id)
    
    for key in kwargs.keys():
        kwargs[key].to_sql(key, engine, schema=proj_id, if_exists='append', index=False, index_label=True, chunksize=None, dtype=None)
    
    print('database: ', time.time()-time1)
    
    return(proj_id)

