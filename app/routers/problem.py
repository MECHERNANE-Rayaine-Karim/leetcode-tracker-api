from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import User
from app.schemas.problem import ProblemAdd, ProblemResponse
from app.models.problem import Problem
from app.services.security import get_current_user
from sqlalchemy import select


router = APIRouter(prefix="/problems")



@router.post("/add", response_model=ProblemResponse)
def create_problem(problem_data : ProblemAdd ,db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    new_problem = Problem(
        user_id = current_user.id,
        title = problem_data.title,
        url = problem_data.url,
        difficulty = problem_data.difficulty,
    )
    db.add(new_problem)
    db.commit()
    db.refresh(new_problem)
    return new_problem