from fastapi import FastAPI

import models
from database import engine
models.Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware
from domain.question import question_router
from domain.user import user_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(question_router.app, tags=['question'])
app.include_router(user_router.app, tags=['user'])
