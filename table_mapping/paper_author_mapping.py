import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class PaperAuthor(Base):
    __tablename__ = 'paper_authors'
    id = Column(Integer, primary_key=True)
    paper_id = Column(Integer)
    author_id = Column(Integer)
    order = Column(Integer)

    def __repr__(self):
        return "<PaperAuthor(paper_id='%s', author_id='%s', order='%s')>" % (self.paper_id, self.author_id, self.order)


