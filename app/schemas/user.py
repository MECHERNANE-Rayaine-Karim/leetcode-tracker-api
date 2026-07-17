from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class UserResponse(BaseModel):
    id: id
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)