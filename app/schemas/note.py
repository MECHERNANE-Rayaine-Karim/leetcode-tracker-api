from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

class NoteAdd(BaseModel):
    content: str


class NoteResponse(BaseModel):
    id: int
    content: str
    written_at: datetime
    model_config = ConfigDict(from_attributes=True)

class NoteEdit(BaseModel):
    content: Optional[str] = None