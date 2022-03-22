import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

from databases.db_engine import engine, metadata


table_author_affilications = Table('author_affilications', metadata,
        Column('id', Integer, primary_key=True)
        Column('author_id', Integer, ),
        Column('affilication_id', Integer, ),
        Column('start_year', Integer, ),
        Column('end_year', Integer, ),
        )

metadata.create_all(engine)

