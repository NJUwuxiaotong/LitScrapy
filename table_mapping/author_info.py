import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    name = Column(String(100))
    dblp_url = Column(String(200))

    def __repr__(self):
        return "<Author(title='%s', name='%s', dblp_url='%s')>" % (self.title, self.name, self.dblp_url)
