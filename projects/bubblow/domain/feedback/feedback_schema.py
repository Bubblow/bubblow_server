from pydantic import BaseModel

class Ask(BaseModel):
    score: int
    content: str
