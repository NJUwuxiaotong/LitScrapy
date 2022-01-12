import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String


engine = create_engine("mysql://root:root@127.0.0.1/literature_base", echo=True)

metadata = MetaData(engine)

student = Table('student', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(50), ),
            Column('age', Integer),
            Column('address', String(10)),
)

metadata.create_all(engine)
