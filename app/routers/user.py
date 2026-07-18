from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin
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
