import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class AuthorAffilication(Base):
    __tablename__ = 'author_affilications'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer)
    affilication_id = Column(Integer)
    start_year = Column(Integer)
    end_year = Column(Integer)

    def __repr__(self):
        return "<AuthorAffilication(author_id='%s', affilication_id='%s', start_year='%s', end_year='%s')>" % (self.author_id, self.affilication_id, self.start_year, self.end_year)

