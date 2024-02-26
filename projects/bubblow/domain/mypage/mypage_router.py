from sqlalchemy.orm import Session
from database import get_db

from fastapi import APIRouter, Depends
from domain.mypage import mypage_crud
from domain.user.user_router import get_current_user
from models import User

app = APIRouter(prefix="/mypage")

@app.get('/record', description="본인이 넣었던 기록 확인")
async def record_view(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return mypage_crud.record(db, current_user)