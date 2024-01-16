from sqlalchemy.orm import Session
from database import get_db

from fastapi import APIRouter, Depends
from domain.question import question_schema, question_crud

app = APIRouter(
    prefix="/question",
)

@app.post(path="/create", description="링크를 넣는 곳", response_model=question_schema.Link)
async def create_link(link: question_schema.Link, db: Session=Depends(get_db)):
    return question_crud.insert_link(link, db)

@app.get(path="/read", description="링크 조회", response_model=question_schema.Link)
async def read_all_link(db: Session=Depends(get_db)):
    return question_crud.list_all_link(db)
