from sqlalchemy.orm import Session
from database import get_db

from fastapi import APIRouter, Depends
from domain.feedback import feedback_crud, feedback_schema
from domain.user.user_router import get_current_user
from models import FeedBack, User

app=APIRouter(
    prefix="/feedback"
)

@app.post("/send", description="링크를 넣는 곳")
def send_feedback(feedback: feedback_schema.Ask, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return feedback_crud.send_feedback(feedback.score, feedback.content, current_user, db)