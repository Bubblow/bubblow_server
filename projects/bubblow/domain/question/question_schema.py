import datetime

from pydantic import BaseModel

class Link(BaseModel):
    link: str
    class Config:
        orm_mode = True

# class LinkList(BaseModel):
#     id: int
#     link: str
#     date: datetime