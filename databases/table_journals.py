import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

from databases.db_engine import engine, metadata


table_journals = Table('journals', metadata,
                Column('id', Integer, primary_key=True),
                Column('name', String(255), ),
                Column('dblp_address', String(255), ),
                Column('issn', String(50), ),
                Column('press', String(50), ),
                )

metadata.create_all(engine)

