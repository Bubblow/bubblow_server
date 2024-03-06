from pydantic import BaseModel, EmailStr, validator
from fastapi import HTTPException

class NewUserForm(BaseModel):
    email: EmailStr
    name: str
    password: str

    @validator('email', 'name', 'password', pre=True)
    def check_empty(cls, v):
        if not v or v.isspace():
            raise HTTPException(status_code=422, detail="필수 항목을 입력해주세요.")
        return v

    @validator('name')
    def validate_username(cls, v):
        if len(v) < 2 or len(v) > 20:
            raise HTTPException(status_code=422, detail="닉네임은 2자 이상 20자 이하이어야 합니다.")
        return v
    
    @validator('password')
    def validate_password(cls, v, values, **kwargs):
        errors = []
        if len(v) < 8:
            errors.append("비밀번호는 8자리 이상이어야 합니다.")
        if not any(char.isdigit() for char in v):
            errors.append("비밀번호에는 최소 한 자리의 숫자가 포함되어야 합니다.")
        if not any(char.isalpha() for char in v):
            errors.append("비밀번호에는 최소 한 자리의 영문자가 포함되어야 합니다.")

        if errors:
            raise HTTPException(status_code=422, detail=" ".join(errors))

        return v

class Token(BaseModel):
    access_token: str
    token_type: str

class SendEmail(BaseModel):
    email: EmailStr
    verification_code: str

class FindEmail(BaseModel):
    email: EmailStr

class EditPassword(BaseModel):
    current_password: str
    new_password: str
    
    @validator('new_password')
    def validate_password(cls, v, values, **kwargs):
        errors = []
        if len(v) < 8:
            errors.append("비밀번호는 8자리 이상이어야 합니다.")
        if not any(char.isdigit() for char in v):
            errors.append("비밀번호에는 최소 한 자리의 숫자가 포함되어야 합니다.")
        if not any(char.isalpha() for char in v):
            errors.append("비밀번호에는 최소 한 자리의 영문자가 포함되어야 합니다.")

        if errors:
            raise HTTPException(status_code=422, detail=" ".join(errors))

        return v

class ResetPassword(BaseModel):
    email: EmailStr
    new_password: str
    
    @validator('new_password')
    def validate_password(cls, v, values, **kwargs):
        errors = []
        if len(v) < 8:
            errors.append("비밀번호는 8자리 이상이어야 합니다.")
        if not any(char.isdigit() for char in v):
            errors.append("비밀번호에는 최소 한 자리의 숫자가 포함되어야 합니다.")
        if not any(char.isalpha() for char in v):
            errors.append("비밀번호에는 최소 한 자리의 영문자가 포함되어야 합니다.")

        if errors:
            raise HTTPException(status_code=422, detail=" ".join(errors))

        return v