from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Attempt, User, Problem
from app.schemas.attempt import AttemptResponse, AttemptDetails, AttemptAdd
from sqlalchemy import select

from app.services.security import get_current_user

router = APIRouter(prefix="/attempts")


@router.get("/", response_model=list[AttemptResponse])
def attempts_list( problem_id: int ,limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0), db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    attempts = db.execute(
        select(Attempt).
        join(Problem, Problem.id == Attempt.problem_id).
        where(Problem.id == problem_id,Problem.user_id == current_user.id ).limit(limit).offset(offset)
    ).scalars().all()

    return attempts

@router.get("/attemptDetails", response_model=AttemptDetails)
def attempt_details( attempt_id: int, db: Session = Depends(get_db),
current_user: User = Depends(get_current_user)):

    attempt = db.execute(
        select(Attempt).
        join(Problem,Attempt.problem_id == Problem.id).
        where( Attempt.id == attempt_id,Problem.user_id == current_user.id)
    ).scalar_one_or_none()

    if attempt is None:
        raise HTTPException(status_code=404, detail="Attempt not found")
    return attempt




@router.post("/add", response_model=AttemptDetails)
def add_attempt(attempt_data : AttemptAdd,db: Session = Depends(get_db),
current_user: User = Depends(get_current_user)):
    problem_check = db.execute(
        select(Problem).where(Problem.id == attempt_data.problem_id, Problem.user_id == current_user.id)).scalar_one_or_none()
    if problem_check is None:
        raise HTTPException(status_code=404, detail="User's problem not found")
    new_attempt = Attempt(
        problem_id = attempt_data.problem_id,
        used_language = attempt_data.used_language,
        code_source = attempt_data.code_source,
        time_complexity = attempt_data.time_complexity,
        space_complexity = attempt_data.space_complexity,
        status = attempt_data.status,
        attempted_at = datetime.now(timezone.utc)
    )
    db.add(new_attempt)
    db.commit()
    db.refresh(new_attempt)
    return new_attempt




