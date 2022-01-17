import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

from databases.db_engine import engine, metadata


table_authors = Table('authors', metadata,
        Column('id', Integer, primary_key=True),
        Column('title', String(100), ),
        Column('name', String(100), ),
        Column('dblp_url', String(200), ),
        )

metadata.create_all(engine)

