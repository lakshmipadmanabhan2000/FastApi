from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#postgres 
SQLALCHEMEY_DATABASE_URL='postgresql://postgres:test1234!@localhost/ToDoApplicationDatabase' #db is in current folder
#mysql
#SQLALCHEMEY_DATABASE_URL='mysql+pymysql://root:test1234!@127.0.0.1:3306/ToDoApplicationDatabase' 
engine=create_engine(SQLALCHEMEY_DATABASE_URL)
sessionLocal=sessionmaker(autoflush=False,autocommit=False, bind=engine)
Base=declarative_base()
