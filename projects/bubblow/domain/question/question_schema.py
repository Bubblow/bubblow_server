from pydantic import BaseModel
import datetime
class NewsLinkSchema(BaseModel):
    link: str
    create_at: datetime.datetime
