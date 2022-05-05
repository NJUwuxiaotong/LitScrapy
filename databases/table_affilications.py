import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

from databases.db_engine import engine, metadata


table_affilications = Table('affilications', metadata,
        Column('id', Integer, primary_key=True),
        Column('department', String(200), ),
        Column('affilication', String(50), ),
        Column('country', String(50), ),
        )

metadata.create_all(engine)




