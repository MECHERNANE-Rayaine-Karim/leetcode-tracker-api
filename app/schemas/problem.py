from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)