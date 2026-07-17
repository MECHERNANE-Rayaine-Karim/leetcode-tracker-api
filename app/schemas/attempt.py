from pydantic import BaseModel, ConfigDict
from app.models.attempt import Language,Complexity,Status
from datetime import datetime

class AttemptAdd(BaseModel):
    problem_id: int
    used_language: Language
    code_source: str
    time_complexity: Complexity
    space_complexity: Complexity
    status: Status

class AttemptResponse(BaseModel):
    id: int
    used_language: Language
    code_source: str
    time_complexity: Complexity
    space_complexity: Complexity
    status: Status
    attempted_at: datetime
    model_config = ConfigDict(from_attributes=True)