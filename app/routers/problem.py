

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status

from app.core.database import get_db, problem_topics
from app.models import User, Topic, Attempt
from app.schemas.problem import ProblemAdd, ProblemResponse, ProblemEdit
from app.models.problem import Problem
from app.schemas.topic import TopicResponse
from app.services.security import get_current_user
from sqlalchemy import select


router = APIRouter(prefix="/problems",dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[ProblemResponse])
def problems_list(limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0), db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    problems = db.execute(select(Problem).where(Problem.user_id == current_user.id).limit(limit).offset(offset)).scalars().all()
    return problems







@router.post("/", response_model=ProblemResponse)
def create_problem(problem_data : ProblemAdd ,topic_ids : list[int] = Query(default=[]),db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    topics = []
    for topic_id in topic_ids :
        topic = db.execute(select(Topic).where(Topic.id == topic_id)).scalar_one_or_none()
        if topic is None:
            raise HTTPException(status_code=404,detail="Topic not found")
        topics.append(topic)
    new_problem = Problem(
        user_id = current_user.id,
        title = problem_data.title,
        url = problem_data.url,
        difficulty = problem_data.difficulty,
    )
    new_problem.topics = topics
    db.add(new_problem)
    db.commit()
    db.refresh(new_problem)
    return new_problem


@router.post("/{problem_id}/topics",)
def link_topic_problem(problem_id: int,topic_id: int ,db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    problem_check = db.execute(
        select(Problem).
        where(Problem.id == problem_id, Problem.user_id == current_user.id)
    ).scalar_one_or_none()
    if problem_check is None:
        raise HTTPException(status_code=404,detail="Problem not found")
    topic = db.execute(select(Topic).where(Topic.id==topic_id)).scalar_one_or_none()
    if topic is None:
        raise HTTPException(status_code=404,detail="Topic not found")
    problem_check.topics.append(topic)
    db.commit()
    return {"message": "Topic linked to problem successfully"}

@router.get("/{problem_id}/topics", response_model= list[TopicResponse])
def get_topics_by_problem(problem_id: int ,db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    problem = db.execute(select(Problem).where(Problem.id==problem_id,Problem.user_id == current_user.id)).scalar_one_or_none()
    if problem is None:
        raise HTTPException(status_code=404,detail="Problem not found")
    topics = db.execute(
        select(Topic).
        join(problem_topics, problem_topics.c.topic_id == Topic.id ).
        join(Problem, problem_topics.c.problem_id == Problem.id).
        where(problem_topics.c.problem_id == problem_id,Problem.user_id == current_user.id)
    ).scalars().all()

    return topics

@router.patch("/{problem_id}",response_model=ProblemResponse)
def edit_problem( problem_id : int ,edited_data: ProblemEdit,db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    problem = db.execute(
        select(Problem).
        where(Problem.id == problem_id, Problem.user_id == current_user.id)
    ).scalar_one_or_none()
    if problem is None:
        raise HTTPException(status_code=404,detail="Problem not found")
    if edited_data.title is not None:
        problem.title = edited_data.title
    if edited_data.url is not None:
        problem.url = edited_data.url
    if edited_data.difficulty is not None:
        problem.difficulty = edited_data.difficulty
    db.commit()
    db.refresh(problem)
    return problem

@router.delete("/{problem_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_problem( problem_id : int ,db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    problem = db.execute(
          select(Problem).
           where( Problem.id == problem_id, Problem.user_id == current_user.id)
    ).scalar_one_or_none()
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    attempts = db.execute(
        select(Attempt).join(Problem,Problem.id == Attempt.problem_id).
        where( Problem.id == problem_id, Problem.user_id == current_user.id)
    ).scalars().all()
    if attempts:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This problem has attempts and cannot be deleted")

    for topic in problem.topics:
        topic.problems.remove(problem)
    db.delete(problem)
    db.commit()



