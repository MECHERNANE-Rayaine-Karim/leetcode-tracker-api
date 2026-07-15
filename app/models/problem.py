from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Enum as SQLAlchemyEnum
from app.core.database import Base
from enum import Enum


class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class Problem(Base):
    __tablename__ = 'problems'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()
    difficulty: Mapped[Difficulty] = mapped_column(SQLAlchemyEnum(Difficulty))
