from typing import Optional

from pydantic import BaseModel, ConfigDict


class TopicAdd(BaseModel):
    name: str

class TopicResponse(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class TopicEdit(BaseModel):
    name: Optional[str] = None