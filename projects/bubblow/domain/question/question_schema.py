from pydantic import BaseModel

class Link(BaseModel):
    link: str
    class Config:
        orm_mode = True
        

class answers(BaseModel):
    content: str