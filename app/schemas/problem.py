from pydantic import BaseModel, ConfigDict

from app.schemas.topic import TopicResponse
from app.models.problem import Difficulty

class ProblemAdd(BaseModel):
    title: str
    url: str
    difficulty: Difficulty


class ProblemResponse(BaseModel):
    id: int
    title: str
    url: str
    difficulty: Difficulty
    topics: list[TopicResponse]

    model_config = ConfigDict(from_attributes=True)