from sqlalchemy.orm import Session

from models import FeedBack, User
from datetime import datetime


def send_feedback(score: int, content: str, user: User, db: Session):
    feedback = FeedBack(
                score = score, 
                content = content, 
                user_id = user.id,
    )
    db.add(feedback)
    db.commit()

    return {
        "score": score,
        "content": content
    }
    