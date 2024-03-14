from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models import User
from domain.user.user_schema import NewUserForm, EditPassword, FindEmail, ResetPassword
from passlib.context import CryptContext
import secrets
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
load_dotenv()

#crypt 해싱 알고리즘을 사용
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#사용자 조희
def get_user(username: str, db: Session) -> User:
    return db.query(User).filter(User.username == username).first()

#이메일 조회
def email_user(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()

#회원가입
def create_user(new_user: NewUserForm, db: Session):
    # 비밀번호 해싱
    hashed_password = pwd_context.hash(new_user.password)
    verification_code = secrets.randbelow(1000000)
    
    # 새로운 User 인스턴스 생성
    user = User(
        username=new_user.name,
        email=new_user.email,
        password=hashed_password,
        verification_code=verification_code,
        verification_code_expires_at=datetime.utcnow() + timedelta(hours=1),  # 인증 코드 만료 시간 설정
        profile_image_path=new_user.profile
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # 이메일 전송
    send_verification_email(user.email, user.verification_code)

#평문 비밀번호와 해시된 비밀번호를 비교
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def send_verification_email(email_to: str, verification_code: str):
    email_from = os.getenv("EMAIL_FROM")
    email_password = os.getenv("EMAIL_PASSWORD")
    
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = "Verify your email address"
    
    body = f"Your verification code is: {verification_code}. Please enter this code to verify your email address."
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_from, email_password)
    text = msg.as_string()
    server.sendmail(email_from, email_to, text)
    server.quit()
    
#마이페이지에서 비밀번호 변경
def edit_password(db: Session, current_user: User, password_update: EditPassword):
    if not pwd_context.verify(password_update.current_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    # 새 비밀번호로 업데이트
    current_user.password = pwd_context.hash(password_update.new_password)
    db.add(current_user)
    db.commit()

#회원탈퇴
def delete_user(db: Session, current_user: User):
    db.delete(current_user)
    db.commit()
    
#비밀번호 찾기
def find_password(db: Session, email: FindEmail):
    user = db.query(User).filter(User.email == email.email).first()
    if not user:
        return {"message": "User not found."}
    
    verification_code = secrets.randbelow(1000000)
    user.verification_code = verification_code
    user.verification_code_expires_at = datetime.utcnow() + timedelta(hours=1)
    db.commit()

    send_verification_email(email.email, verification_code)
    
    return {"message": "A password reset code has been sent if the email is registered."}

#새로운 비밀번호
def reset_password(db: Session, reset_password_data: ResetPassword):
    user = db.query(User).filter(User.email == reset_password_data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    # 새 비밀번호로 업데이트
    user.password = pwd_context.hash(reset_password_data.new_password)
    db.commit()

    return {"message": "Your password has been reset successfully."}