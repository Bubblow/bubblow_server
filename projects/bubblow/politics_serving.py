from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List

# FastAPI 애플리케이션 생성
app = FastAPI()

# 모델 및 TF-IDF 변환기 로드
model = joblib.load('./politics_model/lgbm_model.joblib')
tfidf_vectorizer = joblib.load('./politics_model/tfidf_vectorizer.joblib')

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
    
    # 예측 결과 반환
    return {"prediction": prediction.tolist()}