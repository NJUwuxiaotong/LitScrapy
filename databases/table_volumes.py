import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean

from databases.db_engine import engine, metadata


table_volumes = Table('volumes', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('issn', String(50), ),
                      Column('volume', String(255), ),
                      Column('year', String(50), ),
                      Column('url', String(255), ),
                      Column('is_updated', Boolean, ),)

metadata.create_all(engine)
