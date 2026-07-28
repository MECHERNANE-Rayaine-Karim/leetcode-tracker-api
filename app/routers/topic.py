from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db,problem_topics
from app.models import User, Topic
from app.schemas.problem import ProblemResponse
from app.models.problem import Problem
from app.schemas.topic import TopicResponse, TopicAdd, TopicEdit
from app.services.security import get_current_user, get_current_admin
from sqlalchemy import select

router = APIRouter(prefix="/topics",dependencies=[Depends(get_current_user)])



@router.post("/", response_model=TopicResponse)
def add_topic(topic_data : TopicAdd ,db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)):
    new_topic = Topic(name=topic_data.name)
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)
    return new_topic


@router.get("/{topic_id}/problems", response_model= list[ProblemResponse])
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



@router.patch("/{topic_id}", response_model=TopicResponse)
def edit_topic( topic_id: int ,edited_data: TopicEdit, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)):
    topic = db.execute(select(Topic).where(Topic.id == topic_id)).scalar_one_or_none()
    if topic is None:
        raise HTTPException(status_code=404, detail="topic not found")
    if edited_data.name is not None:
        topic.name = edited_data.name
    db.commit()
    db.refresh(topic)
    return topic


