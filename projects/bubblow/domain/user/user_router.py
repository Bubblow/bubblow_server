import os
from dotenv import load_dotenv

from sqlalchemy.orm import Session
from database import get_db 
from models import User

from fastapi import APIRouter, Depends, HTTPException, Response, status, File, UploadFile
from datetime import datetime, timedelta
from typing import Union
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from domain.user import user_schema, user_crud

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

app = APIRouter(prefix="/user")

# 액세스 토큰 생성 함수
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 회원가입 엔드포인트
@app.post("/signup")
async def signup(new_user: user_schema.NewUserForm, db: Session = Depends(get_db)):
    
    if user_crud.email_user(new_user.email, db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email already exists")
    # 닉네임 중복 검사
    username_exists = user_crud.get_user(new_user.name, db)
    if username_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    user_crud.create_user(new_user, db)    
    return {"detail": "Signup successful"}

# 로그인 엔드포인트
@app.post("/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_crud.email_user(form_data.username, db)  # form_data.username에 이메일 값
    if not user or not user_crud.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    response.set_cookie(key="access_token", value=access_token, httponly=True, expires=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    return user_schema.Token(access_token=access_token, token_type="bearer")

# 로그아웃 엔드포인트
@app.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"detail": "Logout successful"}

#현재 유저 정보 확인 함수
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        
        user = user_crud.email_user(user_email, db)
        
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    
#인증번호 확인
@app.post("/verify_email")
async def verify_email(request_body: user_schema.SendEmail, db: Session = Depends(get_db)):
    email = request_body.email
    verification_code = request_body.verification_code

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.verification_code != verification_code or datetime.utcnow() > user.verification_code_expires_at:
        raise HTTPException(status_code=400, detail="Invalid or expired verification code")
    
    user.is_verified = True
    db.commit()
    return {"detail": "Email verified successfully"}

#비밀번호 변경
@app.put("/edit_password", status_code=status.HTTP_202_ACCEPTED)
async def edit(password: user_schema.EditPassword, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_crud.edit_password(db, current_user=current_user, password_update=password)
    return {"message": "Password updated successfully"}

#회원 탈퇴
@app.delete("/delete")
async def delete(response: Response, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    response.delete_cookie(key="access_token")
    user_crud.delete_user(db, current_user)
    return {"message": "계정이 삭제되었습니다. 쿠키가 삭제되었습니다."}

#비밀번호 찾기
@app.post("/find_password")
async def find(request_body: user_schema.FindEmail, db: Session = Depends(get_db)):
    return user_crud.find_password(db, email=request_body)

@app.post("/reset_password")
async def reset_password(request: user_schema.ResetPassword, db: Session = Depends(get_db)):
    return user_crud.reset_password(db, request)