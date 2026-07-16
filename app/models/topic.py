from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.problem import Problem




class Topic(Base):
    __tablename__ = 'topics'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    problems: Mapped[list["Problem"]] = relationship(secondary= "problem_topics" ,back_populates="topics")

