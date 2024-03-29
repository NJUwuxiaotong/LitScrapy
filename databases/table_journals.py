import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import Table, Column, Integer, String
from databases.db_engine import engine, metadata


table_journals = Table('journals', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('name', String(255), ),
                       Column('dblp_address', String(255), ),
                       Column('issn', String(50), ),
                       Column('press', Integer, ),)

metadata.create_all(engine)
