import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from databases.db_engine import engine


Base = declarative_base()


class Paper(Base):
    __tablename__ = 'papers'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    journal_issn = Column(String(50))
    volume_id = Column(Integer)
    volume = Column(String(50))
    number = Column(String(50))
    start_page = Column(Integer)
    end_page = Column(Integer)
    year = Column(Integer)
    url = Column(String(255))
    doi = Column(String(255))
    dblp_id = Column(String(255))

    def __repr__(self):
        return "<Paper(title='%s', journal_issn='%s', volumn_id='%s', " \
               "volume='%s', number='%s', start_page='%s', end_page='%s', " \
               "year='%s', url='%s', doi='%s', dblp_id='%s')>" % \
               (self.title, self.journal_issn, self.volume_id, self.volume,
                self.number, self.start_page, self.end_page, self.year,
                self.url, self.doi, self.dblp_id)
