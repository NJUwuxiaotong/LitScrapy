import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("mysql://wuxiaotong:root@localhost/literature_base",
                       echo=True)
metadata = MetaData(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()
