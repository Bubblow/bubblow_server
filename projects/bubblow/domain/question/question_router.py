from sqlalchemy.orm import Session
from database import get_db

from fastapi import APIRouter, Depends
from domain.question import question_schema, question_crud
from domain.user.user_router import get_current_user
from models import User

app = APIRouter(
    prefix="/question",
)

@app.post("/create", description="링크를 넣는 곳")
def create_link(Link: question_schema.Link, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return question_crud.insert_answer(Link.link, current_user, db)

@app.get("/read", description="링크 조회")
def read_all_links(db: Session = Depends(get_db)):
    return question_crud.list_all_link(db)
