import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Volume(Base):
    __tablename__ = 'volumes'
    id = Column(Integer, primary_key=True)
    issn = Column(String(50))
    volume = Column(String(255))
    year = Column(String(50))
    url = Column(String(255))
    is_updated = Column(Boolean)

    def __repr__(self):
        return "<Journal(issn='%s', volume='%s', year='%s', url='%s', is_updated='%s')>" % (self.issn, self.volume, self.year, self.url, self.is_updated)


