import time
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def save_db(user_id, engine, **kwargs):
    time1 = time.time() 
    for key in kwargs.keys():
        sql_stmt = "DELETE FROM "+ key + " WHERE user_id='"+user_id+"'"
        with engine.connect() as con:
            con.execute(sql_stmt)
        print(key)
        kwargs[key].to_sql(key, engine, schema='yellow', if_exists='append', index=False)
    
    
    