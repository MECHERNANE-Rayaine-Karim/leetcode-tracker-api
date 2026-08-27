from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from datetime import datetime






class EmailVerificationToken(Base):
    __tablename__ = 'email_verification_tokens'
    id: Mapped[int] = mapped_column(primary_key=True)
    hashed_token: Mapped[str] = mapped_column(unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column()
    expires_at: Mapped[datetime] = mapped_column()
    used_at: Mapped[datetime| None] = mapped_column(nullable=True)
