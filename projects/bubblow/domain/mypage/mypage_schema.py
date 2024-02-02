from pydantic import BaseModel

class Recode(BaseModel):
    link: str
    result: str