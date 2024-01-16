from fastapi import FastAPI, Form, Request

import models
from database import engine
models.Base.metadata.create_all(bind=engine)

import json
import sys
import os
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
templates = Jinja2Templates(directory="templates")
sys.path.append('/Users/hansol/desktop (2)/Bubblow/nt-worker')
app = FastAPI(docs_url="/documentation", redoc_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from Analysis.AnalysisContents import AnalysisContent
from Analysis.AnalysisContents import AnalysisContent
from Analysis.AnalysisTitle import AnalysisTitle
from Analysis.AnalysisScore import AnalysisScore
from feature import Feature

from domain.question import question_router
from domain.user import user_router


app.include_router(question_router.app, tags=['question'])
app.include_router(user_router.app, tags=['user'])

# @app.get("/form_send")
# def form_send(request: Request):
#     return templates.TemplateResponse("form_send.html",{"request":request})

# @app.post("/form_recv")
# def form_recv(request: Request, link: str = Form(...)):
#     newsBuffer = Feature(link)
#     at = AnalysisTitle(newsBuffer[0]['title'])
#     at.PrintMyValue()
#     ac = AnalysisContent(newsBuffer[0]['content'], newsBuffer[0]['provider'], newsBuffer[0]['fix_category'])
#     ac.PrintMyValue()
#     analysis_score = AnalysisScore(at, ac)
#     Journal = analysis_score.Journal
#     Vanilla = analysis_score.Vanilla
#     analysis_score.PrintMyValue()

#     return templates.TemplateResponse("form_recv.html", {"request": request, "data1": newsBuffer, "data2": Journal, "data3": Vanilla})