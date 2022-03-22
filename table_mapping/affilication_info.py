import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Affilication(Base):
    __tablename__ = 'affilications'
    id = Column(Integer, primary_key=True)
    department = Column(String(200))
    city = Column(String(50))
    country = Column(String(50))

    def __repr__(self):
        return "<Affilication(department='%s', city='%s', country='%s')>" % \
               (self.department, self.city, self.country)

