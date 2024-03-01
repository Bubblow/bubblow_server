from sqlalchemy.orm import Session
from models import NewsLink, User
from sqlalchemy import desc
from feature import Feature

def record(db: Session, current_user: User):
    records = db.query(NewsLink.link, NewsLink.analysis_result).filter(NewsLink.user == current_user).order_by(desc(NewsLink.id)).limit(5).all()
    
    results=[]
    
    for link in records:
        newsBuffer = Feature(link.link)
        title = newsBuffer[0]['title']
        content = getFirstChars(newsBuffer[0]['content'])
        analysis_result = link[1]
        # image_url = newsBuffer[0].get('image_url', '')
    
        results.append({
            "link": link.link,
            "title": title,
            "content": content,
            "analysis_result": analysis_result
            # "image_url": image_url,
        })

    email = current_user.email
    username = current_user.username

    return {'email': email, "username": username, "results": results}

#기사내용 35글자까지 저장하는 함수
def getFirstChars(text):
    return text[:35]