from sqlalchemy.orm import Session
from database import get_db

from fastapi import APIRouter, Depends
from domain.question import question_schema, question_crud

app = APIRouter(
    prefix="/question",
)

@app.post("/create", description="링크를 넣는 곳")
def create_link(Link: question_schema.Link, db: Session = Depends(get_db)):
    return question_crud.insert_answer(Link.link, db)

@app.get("/read", description="링크 조회")
def read_all_links(db: Session = Depends(get_db)):
    return question_crud.list_all_link(db)
