from fastapi import FastAPI
import joblib

# 모델 및 TF-IDF 변환기 로드
# model = joblib.load('./politics_model/lgbm_model.joblib')
# tfidf_vectorizer = joblib.load('./politics_model/tfidf_vectorizer.joblib')

import models
from database import engine
models.Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware
from domain.question import question_router
from domain.user import user_router
from domain.mypage import mypage_router
from domain.feedback import feedback_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.app, tags=['user'])
app.include_router(question_router.app, tags=['question'])
app.include_router(mypage_router.app, tags=['mypage'])
app.include_router(feedback_router.app, tags=['feedback'])


# class TextData(BaseModel):
#     title: str
#     content: str
    
# @app.post("/predict")
# async def predict(text_data: TextData):
#     # 입력 데이터 전처리
#     text_input = f"{text_data.title} {text_data.content}"
#     text_input_tfidf = tfidf_vectorizer.transform([text_input])
    
#     # 예측 수행
#     prediction = model.predict(text_input_tfidf)
    
#     # 예측 결과 반환
#     return {"prediction": int(prediction[0])}