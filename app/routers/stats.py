from datetime import date, timedelta

from sqlalchemy import func, select, distinct

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Attempt, Problem, User
from app.models.attempt import Status
from app.schemas.stats import StatsResponse
from app.services.security import get_current_user

router = APIRouter(prefix="/stats")

@router.get("/", response_model=StatsResponse)
def get_statistics(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    total_problems_solved = db.execute(
        select(func.count(distinct(Attempt.problem_id))).
        join(Problem,Problem.id == Attempt.problem_id).
        where(Problem.user_id == current_user.id,Attempt.status == Status.SOLVED)
    ).scalar_one()
    results = db.execute(
        select(Problem.difficulty,func.count(distinct(Problem.id))).
        where(Problem.user_id == current_user.id).
        group_by(Problem.difficulty)
    ).all()
    problems_by_difficulty = {row[0]: row[1] for row in results}
    results = db.execute(
        select(Attempt.status, func.count(distinct(Attempt.id))).
        join(Problem, Problem.id == Attempt.problem_id).
        where(Problem.user_id == current_user.id).
        group_by(Attempt.status)
    ).all()
    total_attempts = db.execute(
        select(func.count(distinct(Attempt.id))).
        join(Problem, Problem.id == Attempt.problem_id).
        where(Problem.user_id == current_user.id)
    ).scalar_one()
    attempts_by_status = {row[0]: row[1] for row in results}
    results = db.execute(
        select(Attempt.used_language, func.count(distinct(Attempt.id))).
        join(Problem, Problem.id == Attempt.problem_id).
        where(Problem.user_id == current_user.id).
        group_by(Attempt.used_language)
    ).all()
    attempts_by_language = {row[0]: row[1] for row in results}
    active_days = db.execute(
        select(distinct(func.date(Attempt.attempted_at))).
        join(Problem,Problem.id == Attempt.problem_id).
        where(Problem.user_id == current_user.id).
        order_by(func.date(Attempt.attempted_at))
    ).scalars().all()

    current_streak = 1
    longest_streak = 1 if active_days else 0
    for i in range( 0, len(active_days)-1):
        if active_days[i+1] == active_days[i]+timedelta(days=1) :
            current_streak += 1
        else:
            current_streak = 1
        longest_streak = max(longest_streak, current_streak)
    if not active_days:
        current_streak = 0
    elif active_days[-1] != date.today() and active_days[-1] != date.today()-timedelta(days=1):
        current_streak = 0


    statistics = StatsResponse(
        total_problems_solved = total_problems_solved,
        problems_by_difficulty =  problems_by_difficulty,
        total_attempts = total_attempts,
        attempts_by_status = attempts_by_status,
        attempts_by_language =  attempts_by_language,
        current_streak = current_streak,
        longest_streak = longest_streak
    )
    return statistics