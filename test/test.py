import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("mysql://root:root@127.0.0.1/literature_base", echo=False)
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    age = Column(Integer)
    address = Column(String(100))

#student1 = Student(id=1001, name='ling', age=25, address="beijing")
#student2 = Student(id=1002, name='molin', age=18, address="jiangxi")
#student3 = Student(id=1003, name='karl', age=16, address="suzhou")

#session.add_all([student1, student2, student3])
#session.commit()

my_stu = session.query(Student).filter_by(name="ling").first()
print(my_stu.id, my_stu.name, my_stu.age, my_stu.address)

session.close()



