import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

from databases.db_engine import engine, metadata


journals = Table('papers', metadata,
                Column('id', Integer, primary_key=True)
                Column('tilte', String(255), ),
                Column('journal_issn', String(50), ),
                Column('volume', String(50), ),
                Column('number', String(50), ),
                Column('start_page', Integer, ),
                Column('end_page', Integer, ),
                Column('year', Integer, ),
                Column('url', String(255), ),
                Column('doi', String(255), ),
                Column('key_words', String(255), ),
                Column('abstract', String(2048), ),
                )

metadata.create_all(engine)

