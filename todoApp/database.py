from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
SQLALCHEMEY_DATABASE_URL='sqlite:///./todosapp.db' #db is in current folder
engine=create_engine(SQLALCHEMEY_DATABASE_URL,
                     connect_args={'check_same_thread':False })
sessionLocal=sessionmaker(autoflush=False,autocommit=False, bind=engine)
Base=declarative_base()
