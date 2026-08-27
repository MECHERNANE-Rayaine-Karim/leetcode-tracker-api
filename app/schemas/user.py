from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    username: str
    password: str

class TokenRequest(BaseModel):
    email: EmailStr

class PasswordResetRequest(BaseModel):
    raw_token: str
    new_password: str
class EmailVerificationRequest(BaseModel):
    raw_token: str