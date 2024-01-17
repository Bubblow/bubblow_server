from sqlalchemy.orm import Session

from models import Question
from domain.question.question_schema import Link
from datetime import datetime
from feature import Feature

#LinkList
import sys, json
sys.path.append('/Users/hansol/desktop (2)/Bubblow/nt-worker')
from Analysis.AnalysisContents import AnalysisContent
from Analysis.AnalysisContents import AnalysisContent
from Analysis.AnalysisTitle import AnalysisTitle
from Analysis.AnalysisScore import AnalysisScore


def insert_answer(link: str, db: Session):
    newsBuffer = Feature(link)
    at = AnalysisTitle(newsBuffer[0]['title'])
    at.PrintMyValue()
    ac = AnalysisContent(newsBuffer[0]['content'], newsBuffer[0]['provider'], newsBuffer[0]['fix_category'])
    ac.PrintMyValue()
    analysis_score = AnalysisScore(at, ac)
    Journal = analysis_score.Journal
    Vanilla = analysis_score.Vanilla
    analysis_score.PrintMyValue()
    content=json.dumps(Journal)
    answer = Question(link=link, content=content, create_date=datetime.utcnow())
    db.add(answer)
    db.commit()
    
    return answer

def list_all_link(db: Session):
    contents = db.query(Question.content).all()
    print(contents)
    return [content[0] for content in contents]
    # [LinkList(id=row.id, link=row.link, date=row.date) for row in lists]