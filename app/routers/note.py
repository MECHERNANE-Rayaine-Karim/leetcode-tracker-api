from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import User, Note, Attempt
from app.schemas.note import NoteResponse, NoteAdd
from app.models.problem import Problem
from app.services.security import get_current_user
from sqlalchemy import select




router = APIRouter(prefix="/notes")


@router.get("/getNotes", response_model=list[NoteResponse])
def notes_list( attempt_id: int ,limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0), db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    notes = db.execute(
        select(Note).join(Attempt,Note.attempt_id==Attempt.id).
        join(Problem,Problem.id==Attempt.problem_id).
        where(Problem.user_id == current_user.id,Note.attempt_id == attempt_id).
        limit(limit).offset(offset)
    ).scalars().all()
    return notes




@router.post("/addNote", response_model=NoteResponse)
def add_note( note_data: NoteAdd,db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user)):
    attempt = db.execute(
        select(Attempt).join(Problem,Attempt.problem_id==Problem.id).
        where(Problem.user_id == current_user.id,Attempt.id == note_data.attempt_id)
    ).scalar_one_or_none()
    if attempt is None:
        raise HTTPException(status_code=404, detail="attempt not found")

    new_note = Note(
        attempt_id = note_data.attempt_id,
        content = note_data.content,
        written_at = datetime.now()
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note





