from sqlalchemy.orm import Session
from models import NewsLink, User

def record(db: Session, current_user: User):
    records = db.query(NewsLink.link, NewsLink.analysis_result).filter(NewsLink.user == current_user).all()
    links = [record[0] for record in records]
    results = [record[1] for record in records]

    email = current_user.email
    username = current_user.username

    print(results, email)
    return {'email': email, "username": username,  "links": links, "results": results}