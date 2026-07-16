
from sqlalchemy import Column,Integer,String,Float,DateTime,ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class User(Base):
    __tablename__ = "users"

    id=Column(Integer,primary_key=True,index=True,nullable=True,autoincrement=True)
    user_name=Column(String)
    email=Column(String,index=True)
    first_name=Column(String)
    last_name=Column(String)
    hashed_password=Column(String)
    role = Column(String,nullable=True)



class Expense(Base):
    __tablename__ = "expenses"

    id=Column(Integer,primary_key=True,nullable=True,autoincrement=True,index=True)
    amount=Column(Float)
    title=Column(String)
    time=Column(DateTime)
    owner_id = Column(Integer)






