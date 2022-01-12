import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("mysql://root:root@127.0.0.1/literature_base", echo=True)
metadata = MetaData(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()


