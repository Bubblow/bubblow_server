from sqlalchemy.orm import Session

from models import NewsLink, User
from datetime import datetime
from feature import Feature
from sqlalchemy import desc

import sys, json
sys.path.append(r'C:\Users\서아영\Desktop\버블로우서버\bubblow_server\projects\nt-worker')
from Analysis.AnalysisContents import AnalysisContent
from Analysis.AnalysisContents import AnalysisContent
from Analysis.AnalysisTitle import AnalysisTitle
from Analysis.AnalysisScore import AnalysisScore

# 신뢰도 분석 함수
def insert_answer(link: str, user: User, db: Session):
    newsBuffer = Feature(link)
    title = newsBuffer[0]['title']
    content = newsBuffer[0]['content']
    
    at = AnalysisTitle(title)
    ac = AnalysisContent(content, newsBuffer[0]['provider'], newsBuffer[0]['fix_category'])
    analysis_score = AnalysisScore(at, ac)
    Journal = analysis_score.Journal #신뢰도 점수
    Vanilla = analysis_score.Vanilla #알고리즘 점수
    # at.PrintMyValue()
    # ac.PrintMyValue()
    # analysis_score.PrintMyValue()
    
    analysis_result_json = json.dumps(Journal)
    
    new_news_link = NewsLink(
        link=link,
        analysis_result=analysis_result_json,  # 분석 결과 저장
        user_id=user.id  # 사용자 ID 설정
    )
    db.add(new_news_link)
    db.commit()

    return {
        "analysis_result": new_news_link.analysis_result
    }

# 최근 분석 기사 최신 5개
def read_link(db: Session):
    links = db.query(NewsLink).order_by(desc(NewsLink.id)).limit(5).all()
    results = [] 

    for link in links:
        newsBuffer = Feature(link.link)
        title = newsBuffer[0]['title']
        content = getFirstChars(newsBuffer[0]['content'])
        # image_url = newsBuffer[0].get('image_url', '')
        
        results.append({
            "link": link.link,
            "title": title,
            "content": content,
            # "image_url": image_url,
        })
    return results

#기사내용 35글자까지 저장하는 함수
def getFirstChars(text):
    return text[:35]
