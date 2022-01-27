import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

from databases.db_engine import engine, metadata


table_papers = Table('papers', metadata,
                Column('id', Integer, primary_key=True),
                Column('title', String(255), ),
                Column('journal_issn', String(50), ),
                Column('volume_id', Integer, ),
                Column('volume', String(50), ),
                Column('number', String(50), ),
                Column('start_page', Integer, ),
                Column('end_page', Integer, ),
                Column('year', Integer, ),
                Column('url', String(255), ),
                Column('doi', String(255), ),
                )



metadata.create_all(engine)

