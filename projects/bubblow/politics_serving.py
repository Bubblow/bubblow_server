from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List
import os

# # FastAPI 애플리케이션 생성
# app = FastAPI()
# FastAPI 애플리케이션 생성
app = FastAPI()

# 현재 파일의 디렉토리 경로 가져오기
dir_path = os.path.dirname(os.path.realpath(__file__))

# # 모델 및 TF-IDF 변환기 로드
# model = joblib.load('lgbm_model.joblib')
# tfidf_vectorizer = joblib.load('tfidf_vectorizer.joblib')
# 모델 및 TF-IDF 변환기 로드
model = joblib.load(os.path.join(dir_path, 'politics_model/lgbm_model.joblib'))
tfidf_vectorizer = joblib.load(os.path.join(dir_path, 'politics_model/tfidf_vectorizer.joblib'))

# 데이터를 받기 위한 Pydantic 모델 정의
class Item(BaseModel):
    data: str

# 예측을 위한 엔드포인트 정의
@app.post("/predict/")
async def predict(item: Item):
    # TF-IDF 변환
    data_tfidf = tfidf_vectorizer.transform([item.data])
    
    # 모델 예측
    prediction = model.predict(data_tfidf)
    probabilities = model.predict_proba(data_tfidf).tolist()[0]
    
    # 예측 결과와 예측 확률 반환
    return {"prediction": prediction.tolist(), "probabilities": probabilities}