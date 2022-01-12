import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Journal(Base):
    __tablename__ = 'journals'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    dblp_address = Column(String(255))
    issn = Column(String(50))
    press = Column(String(50))

    def __repr__(self):
        return "<Journal(name='%s', dblp_address='%s', issn='%s', press='%s')>" % (self.name, self.dblp, self.isbn, self.press)

