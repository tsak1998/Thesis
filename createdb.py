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
        engine = create_engine("mysql+pymysql://root:pass@localhost:3306/"+projCode)
        engine.connect()

        #need to clear tables
    except:
        engine = create_engine("mysql+pymysql://root:pass@localhost:3306/yellow")
        engine.execute("CREATE DATABASE "+projCode) #create db
        engine.execute("USE "+projCode) # select new db
        #tables, the ones in table.py
        create_tables(engine)
    
    return engine


def createDB(user_id, **kwargs):
    time1 = time.time()
    engine = create_engine("mysql+pymysql://root:pass@localhost:3306/yellow")
    
    for key in kwargs.keys():
        #sql_stmt = "DELETE FROM `yellow`.`"+ key +"` WHERE (`user_id`=`"+user_id+"`);"
        sql_stmt = "DELETE FROM "+ key + " WHERE user_id='"+user_id+"'"
        # s FROM `yellow`.`elements` WHERE (`id` = '3');

        with engine.connect() as con:
            rs = con.execute(sql_stmt)
        print(rs)
        kwargs[key].to_sql(key, engine, schema='yellow', if_exists='append', index=False, index_label=True, chunksize=None, dtype=None)
    
    print('database: ', time.time()-time1)
    
   
#init_db('_0000125')