from sqlalchemy import Column, Integer, String, DateTime, VARCHAR, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username=Column(VARCHAR(10), unique=True, nullable=False)
    password = Column(VARCHAR(100), nullable=False)
    email = Column(VARCHAR(100), unique=True, nullable=False)
    
class NewsLink(Base):
    __tablename__ = "news_links"

    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String, nullable=False)
    analysis_result = Column(Text, nullable=True)  # 분석 결과, JSON 형식의 문자열로 저장
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", backref="news_links")  # User 모델과의 관계 설정
    create_at = Column(DateTime, nullable=False, default=datetime.now)

class FeedBack(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True)
    score = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    create_at = Column(DateTime, nullable=False, default=datetime.now)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", backref="feedback")
