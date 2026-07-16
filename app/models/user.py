from sqlalchemy.orm import Mapped, mapped_column
from typing import TYPE_CHECKING
from app.core.database import Base
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from app.models.problem import Problem



class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    problems: Mapped[list["Problem"]] = relationship(back_populates="user")

