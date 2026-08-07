from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.topic import TopicResponse
from app.models.problem import Difficulty

class ProblemAdd(BaseModel):
    title: str = Field(min_length=1)
    url: str = Field(min_length=1)
    difficulty: Difficulty


class ProblemResponse(BaseModel):
    id: int
    title: str
    url: str
    difficulty: Difficulty
    topics: list[TopicResponse]
    model_config = ConfigDict(from_attributes=True)

class ProblemEdit(BaseModel):
    title: Optional[str] = Field(min_length=1)
    url: Optional[str] = Field(min_length=1)
    difficulty: Optional[Difficulty] = None