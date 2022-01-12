import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

from databases.db_engine import engine, metadata


journals = Table('paper_authors', metadata,
                Column('id', Integer, primary_key=True)
                Column('paper_id', Integer, ),
                Column('author_id', Integer), ),
                Column('order', Integer, ),
                )

metadata.create_all(engine)




