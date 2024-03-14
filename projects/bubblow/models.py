from sqlalchemy import Column, Integer, String, DateTime, VARCHAR, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta

from database import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(10), unique=True, nullable=False)
    password = Column(VARCHAR(100), nullable=False)
    email = Column(VARCHAR(100), unique=True, nullable=False)
    is_verified = Column(Boolean, default=False)  # 이메일 인증 상태
    verification_code = Column(VARCHAR(100), nullable=True)  # 이메일 인증 코드
    verification_code_expires_at = Column(DateTime, nullable=True)  # 인증 코드 만료 시간
    profile_image_path = Column(String, nullable=True)  # 프로필 이미지 파일 경로
    news_links = relationship("NewsLink", backref="user", cascade="all, delete, delete-orphan")
    feedback = relationship("FeedBack", backref="user")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 이메일 인증 코드 생성 시, 만료 시간
        self.verification_code_expires_at = datetime.utcnow() + timedelta(hours=1)
    
class NewsLink(Base):
    __tablename__ = "news_links"

    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String, nullable=False)
    analysis_result = Column(Text, nullable=True)  # 분석 결과, JSON 형식의 문자열로 저장
    create_at = Column(DateTime, nullable=False, default=datetime.now)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

class FeedBack(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True)
    score = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    create_at = Column(DateTime, nullable=False, default=datetime.now)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    
