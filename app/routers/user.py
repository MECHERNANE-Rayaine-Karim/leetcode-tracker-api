import hashlib
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
import secrets
from starlette import status

from app.core.database import get_db
from app.models.password_reset_token import PasswordResetToken
from app.schemas.user import UserCreate, UserResponse, UserLogin, PasswordResetRequest
from app.models.user import User
from app.services.security import hash_password, verify_password, create_access_token
from sqlalchemy import select


router = APIRouter(prefix="/users")




@router.post("/register", response_model=UserResponse)
def register_user(user_data : UserCreate ,db: Session = Depends(get_db)):

    new_user = User(
        username = user_data.username,
        email = user_data.email,
        hashed_password = hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login_user(user_data : UserLogin,db: Session = Depends(get_db)):

    user = db.execute(select(User).where(User.username == user_data.username)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    else:
        if verify_password(user_data.password, user.hashed_password):
            return create_access_token({"sub": user_data.username})
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")


@router.post("/forgot_password")
def forgot_password( data: PasswordResetRequest ,db: Session = Depends(get_db)):
    user_id = db.execute(select(User.id).where(User.email == data.email)).scalar_one_or_none()
    if user_id:
        token = db.execute(
            select(PasswordResetToken).
            where(PasswordResetToken.user_id == user_id,
                  PasswordResetToken.expires_at > datetime.now(),
                  PasswordResetToken.used_at.is_(None))
        ).scalars().all()
        for existing_token in token:
            db.delete(existing_token)
        db.commit()
        raw_token = secrets.token_urlsafe(32)
        hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()
        new_password_reset_token = PasswordResetToken(
            hashed_token=hashed_token,
            user_id= user_id,
            created_at= datetime.now(),
            expires_at= datetime.now() + timedelta(minutes=30),
            used_at= None,
        )
        db.add(new_password_reset_token)
        db.commit()
        db.refresh(new_password_reset_token)
        print(f"Password reset link: http://localhost:5173/reset-password?token={raw_token}")
    if user_id is None:
        hashlib.sha256(secrets.token_urlsafe(32).encode()).hexdigest()
    return "token has been sent"



