from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column
from typing import TYPE_CHECKING
from app.core.database import Base
from sqlalchemy.orm import relationship
from enum import Enum


if TYPE_CHECKING:
    from app.models.problem import Problem


class Role(Enum):
    ADMIN = "admin"
    REGULAR = "regular"




class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    role: Mapped[Role] = mapped_column(SQLAlchemyEnum(Role),default= Role.REGULAR,server_default="REGULAR")
    problems: Mapped[list["Problem"]] = relationship(back_populates="user")

