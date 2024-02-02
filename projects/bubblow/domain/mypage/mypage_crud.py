from sqlalchemy.orm import Session
from models import Question, User


def record(db: Session, current_user: User):
    print(current_user)
    links = db.query(Question.link).filter(Question.user == current_user).all()
    results = db.query(Question.content).filter(Question.user == current_user).all()
    link = [link[0] for link in links]  # 각 link 튜플의 첫 번째 요소를 추출
    result = [content[0] for content in results]  # 각 result 튜플의 첫 번째 요소를 추출

    return {"links": link, "results": result}

    