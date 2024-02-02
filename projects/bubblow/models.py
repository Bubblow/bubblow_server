from sqlalchemy import Column, Integer, String, DateTime, VARCHAR, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base

class Question(Base):
    __tablename__ = "question"
    
    id=Column(Integer, primary_key=True, autoincrement=True)
    link=Column(String, nullable=False)
    content=Column(Text, nullable=False)
    create_date=Column(DateTime, nullable=False, default=datetime.now)

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username=Column(VARCHAR(10), unique=True, nullable=False)
    password = Column(VARCHAR(100), nullable=False)
    email = Column(VARCHAR(100), unique=True, nullable=False)
    
class Post(Base):
	__tablename__="post"

	id = Column(Integer, primary_key=True, autoincrement=True)
	title=Column(String, nullable=False)
	content=Column(Text, nullable=False)