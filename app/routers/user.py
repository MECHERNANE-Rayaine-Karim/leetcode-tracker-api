import hashlib
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
import secrets
from starlette import status

from app.core.database import get_db
from app.models.password_reset_token import PasswordResetToken
from app.schemas.user import UserCreate, UserResponse, UserLogin, PasswordResetRequest, TokenRequest
from app.models.user import User
from app.services.security import hash_password, verify_password, create_access_token
from sqlalchemy import select
import resend
from app.core.config import settings
from sqlalchemy.exc import IntegrityError


resend.api_key = settings.resend_api_key
router = APIRouter(prefix="/users")




@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already registered"
        )
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login_user(user_data : UserLogin,db: Session = Depends(get_db)):

    user = db.execute(select(User).where(User.username == user_data.username)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    else:
        if verify_password(user_data.password, user.hashed_password):
            return create_access_token({"sub": user.username,"role" : user.role.value})
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")


@router.post("/forgot_password")
def forgot_password( data: TokenRequest ,db: Session = Depends(get_db)):
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
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": [data.email],
            "subject": "Reset your password",
            "html": f"<p>Click the link below to reset your password. This link expires in 30 minutes.</p><p><a href='http://localhost:5173/reset_password?token={raw_token}'>Reset Password</a></p>",
        })
    if user_id is None:
        hashlib.sha256(secrets.token_urlsafe(32).encode()).hexdigest()
    return "token has been sent"


@router.post("/reset_password")
def reset_password( data: PasswordResetRequest ,db: Session = Depends(get_db)):
    hashed_token = hashlib.sha256(data.raw_token.encode()).hexdigest()
    password_reset = db.execute(select(PasswordResetToken).where(PasswordResetToken.hashed_token == hashed_token,PasswordResetToken.used_at.is_(None),PasswordResetToken.expires_at > datetime.now())).scalar_one_or_none()
    if password_reset is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect token" )
    user = db.execute(select(User).where(User.id == password_reset.user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = hash_password(data.new_password)
    db.commit()
    db.refresh(user)
    password_reset.used_at = datetime.now()
    db.commit()
    db.refresh(password_reset)

    return "password has been changed"


