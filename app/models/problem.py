from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Enum as SQLAlchemyEnum
from app.core.database import Base
from enum import Enum
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.topic import Topic
    from app.models.attempt import Attempt


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
    user: Mapped["User"] = relationship(back_populates="problems")
    attempts: Mapped[list["Attempt"]] = relationship(back_populates="problem")
    topics: Mapped[list["Topic"]] = relationship(secondary = "problem_topics" ,back_populates="problems")

