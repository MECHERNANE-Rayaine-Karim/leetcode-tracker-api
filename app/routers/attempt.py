from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status

from app.core.database import get_db
from app.models import Attempt, User, Problem, Note
from app.schemas.attempt import AttemptResponse, AttemptDetails, AttemptAdd
from sqlalchemy import select

from app.services.security import get_current_user

router = APIRouter(prefix="/problems/{problem_id}",dependencies=[Depends(get_current_user)])


@router.get("/attempts", response_model=list[AttemptResponse])
def attempts_list( problem_id: int ,limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0), db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    attempts = db.execute(
        select(Attempt).
        join(Problem, Problem.id == Attempt.problem_id).
        where(Problem.id == problem_id,Problem.user_id == current_user.id ).limit(limit).offset(offset)
    ).scalars().all()

    return attempts

@router.get("/attempts/{attempt_id}", response_model=AttemptDetails)
def attempt_details( problem_id: int ,attempt_id: int, db: Session = Depends(get_db),
current_user: User = Depends(get_current_user)):

    attempt = db.execute(
        select(Attempt).
        join(Problem,Attempt.problem_id == Problem.id).
        where( Attempt.id == attempt_id,Problem.id == problem_id,Problem.user_id == current_user.id)
    ).scalar_one_or_none()

    if attempt is None:
        raise HTTPException(status_code=404, detail="Attempt not found")
    return attempt




@router.post("/attempts", response_model=AttemptDetails)
def add_attempt(problem_id:int ,attempt_data : AttemptAdd,db: Session = Depends(get_db),
current_user: User = Depends(get_current_user)):
    problem_check = db.execute(
        select(Problem).where(Problem.id == problem_id, Problem.user_id == current_user.id)).scalar_one_or_none()
    if problem_check is None:
        raise HTTPException(status_code=404, detail="User's problem not found")
    new_attempt = Attempt(
        problem_id = problem_id,
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

@router.delete("/attempts/{attempt_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_attempt( problem_id: int ,attempt_id: int, db: Session = Depends(get_db),
current_user: User = Depends(get_current_user)):
    attempt = db.execute(
        select(Attempt).
        join(Problem, Attempt.problem_id == Problem.id).
        where(Attempt.id == attempt_id, Problem.id == problem_id, Problem.user_id == current_user.id)
    ).scalar_one_or_none()
    if attempt is None:
        raise HTTPException(status_code=404, detail="Attempt not found")
    notes = db.execute(
        select(Note).join(Attempt, Attempt.id == Note.attempt_id).
        join(Problem, Attempt.problem_id == Problem.id).
        where(Attempt.id == attempt_id, Problem.id == problem_id, Problem.user_id == current_user.id)
    ).scalars().all()
    if  notes:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This attempt has notes and cannot be deleted")
    db.delete(attempt)
    db.commit()
