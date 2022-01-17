import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

from databases.db_engine import engine, metadata


table_paper_author_affilications = Table(
        'paper_author_affilications', metadata,
        Column('id', Integer, primary_key=True)
        Column('paper_id', Integer, ),
        Column('author_affilication_id', Integer, ),
        Column('order', Integer, ),
        )

metadata.create_all(engine)




