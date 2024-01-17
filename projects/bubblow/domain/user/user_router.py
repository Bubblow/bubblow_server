import os
from dotenv import load_dotenv

from sqlalchemy.orm import Session
from database import get_db

from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from datetime import datetime, timedelta
from typing import Union
from domain.user import user_schema, user_crud

from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = APIRouter(
    prefix="/user"
)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post(path="/signup")
async def signup(new_user: user_schema.NewUserForm, db: Session = Depends(get_db)):
    
    user = user_crud.get_user(new_user.email, db)
    
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    
    user_crud.create_user(new_user, db)    
        
    return HTTPException(status_code=status.HTTP_200_OK, detail="Signup successful")


@app.post(path="/login")
async def login(response: Response, login_form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_crud.get_user(login_form.username, db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user or password")
    
    res = user_crud.verify_password(login_form.password, user.password)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    
    response.set_cookie(key="access_token", value=access_token, expires=access_token_expires, httponly=True)
    
    if not res:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user or password")
    
    return user_schema.Token(access_token=access_token, token_type="bearer")

@app.get(path="/logout")
async def logout(response: Response, request: Request):
    access_token=request.cookies.get("access_token")
    
    response.delete_cookie(key="access_token")
    return HTTPException(status_code=status.HTTP_200_OK, detail="Logout successful")

