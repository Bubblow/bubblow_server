from  sqlalchemy import Column, Integer, String, Text, DateTime, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base

class Question(Base):
    __tablename__ = "question"
    
    id=Column(Integer, primary_key=True, autoincrement=True)
    link=Column(String, nullable=False)
    create_date=Column(DateTime, nullable=False, default=datetime.now)

class Answer(Base):
    __tablename__ = "answer"
    
    id=Column(Integer, primary_key=True, autoincrement=True)
    content=Column(VARCHAR(255), nullable=False)
    create_date=Column(DateTime, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship("Question", backref="answers")

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username=Column(VARCHAR(10), unique=True, nullable=False)
    password = Column(VARCHAR(100), nullable=False)
    email = Column(VARCHAR(100), unique=True, nullable=False)
    