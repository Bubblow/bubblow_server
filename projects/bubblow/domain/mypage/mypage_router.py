from sqlalchemy.orm import Session
from database import get_db

from fastapi import APIRouter, Depends
from domain.mypage import mypage_crud, mypage_schema
from domain.user.user_router import get_current_user
from models import User

app=APIRouter(
    prefix="/mypage"
)

@app.get('/record', description="기록 확인")
async def record(db:Session=Depends(get_db), current_user: User = Depends(get_current_user)):
    return mypage_crud.record(db, current_user)