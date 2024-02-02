from sqlalchemy.orm import Session

from models import User
from domain.user.user_schema import NewUserForm

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()

def email_user(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

def create_user(new_user: NewUserForm, db: Session):
    user = User(
        username=new_user.name,
        email=new_user.email,
        password=pwd_context.hash(new_user.password),
    )
    db.add(user)
    db.commit()
    
def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)
