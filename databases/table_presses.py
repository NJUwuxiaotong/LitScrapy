import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

from databases.db_engine import engine, metadata


table_presses = Table('presses', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('name', String(50), ),
                      Column('url', String(100), ),)

metadata.create_all(engine)
