from pydantic import BaseModel, EmailStr

class Recode(BaseModel):
    link: str
    result: str
    email: EmailStr
    username: str
    profile: str

class NicknameUpdate(BaseModel):
    username: str