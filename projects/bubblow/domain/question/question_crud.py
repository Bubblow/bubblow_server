from sqlalchemy.orm import Session

from models import Question
from domain.question.question_schema import Link
#LinkList

def insert_link(create_link: Link, db: Session):
    link = Question(
        link = create_link.link,
    )
    db.add(link)
    db.commit()
    
    return link.id

def list_all_link(db: Session):
    lists=db.query(Question).all()
    return lists
    # [LinkList(id=row.id, link=row.link, date=row.date) for row in lists]