from sqlalchemy.orm import Session
from database import get_db

from fastapi import APIRouter, Depends
from domain.post import post_schema, post_crud

app = APIRouter(
    prefix="/post",
)

@app.post(path="/create", description="post 생성")
async def post_create(new_post:post_schema.Post, db:Session = Depends(get_db)):
	return post_crud.insert_post(new_post, db)

@app.get(path="/read", description="post 읽기")
async def post_read(db:Session = Depends(get_db)):
    return post_crud.read_post(db)