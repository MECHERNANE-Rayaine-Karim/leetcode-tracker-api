from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.services.security import hash_password

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
def login_user(db: Session = Depends(get_db)):
    pass
