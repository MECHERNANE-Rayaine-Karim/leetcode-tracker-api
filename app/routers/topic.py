from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db,problem_topics
from app.models import User, Topic
from app.schemas.problem import ProblemAdd, ProblemResponse
from app.models.problem import Problem
from app.schemas.topic import TopicResponse, TopicAdd
from app.services.security import get_current_user
from sqlalchemy import select, Row

router = APIRouter(prefix="/topics")



@router.post("/add", response_model=TopicResponse)
def add_topic(topic_data : TopicAdd ,db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    if current_user.id != settings.admin_id:
        raise HTTPException(status_code=403,detail="invalid permission")
    new_topic = Topic(name=topic_data.name)
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)
    return new_topic


@router.post("/linkProblemTopic",)
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


@router.get("/getProblems", response_model= list[ProblemResponse])
def get_problems_by_topic(topic_id: int ,db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    topic = db.execute(select(Topic).where(Topic.id==topic_id)).scalar_one_or_none()
    if topic is None:
        raise HTTPException(status_code=404,detail="Topic not found")
    problems = db.execute(
        select(Problem).
        join(problem_topics, problem_topics.c.problem_id == Problem.id ).
        where(problem_topics.c.topic_id == topic_id,Problem.user_id == current_user.id)
    ).scalars().all()

    return problems

@router.get("/getTopics", response_model= list[TopicResponse])
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




