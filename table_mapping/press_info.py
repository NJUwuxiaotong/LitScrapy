import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Press(Base):
    __tablename__ = 'presses'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    url = Column(String(100))

    def __repr__(self):
        return "<Press(name='%s', url='%s')>" % \
               (self.name, self.url)
