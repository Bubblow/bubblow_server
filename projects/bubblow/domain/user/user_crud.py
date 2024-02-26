from sqlalchemy.orm import Session
from models import User
from domain.user.user_schema import NewUserForm
from passlib.context import CryptContext

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
    
    # 새로운 User 인스턴스 생성
    user = User(
        username=new_user.name,
        email=new_user.email,
        password=hashed_password,
    )
    db.add(user)
    db.commit()

#평문 비밀번호와 해시된 비밀번호를 비교
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
