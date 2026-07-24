from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.attempt import Attempt


class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column()
    written_at: Mapped[datetime] = mapped_column()
    attempt_id: Mapped[int] = mapped_column(ForeignKey("attempts.id"))
    attempt: Mapped["Attempt"] = relationship(back_populates="notes")

