from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status

from app.core.database import get_db
from app.models import User, Note, Attempt
from app.schemas.note import NoteResponse, NoteAdd, NoteEdit
from app.models.problem import Problem
from app.services.security import get_current_user
from sqlalchemy import select




router = APIRouter(prefix="/problems/{problem_id}/attempts/{attempt_id}",dependencies=[Depends(get_current_user)])


@router.get("/notes", response_model=list[NoteResponse])
def notes_list( attempt_id: int , problem_id: int,limit: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0), db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    notes = db.execute(
        select(Note).join(Attempt,Note.attempt_id==Attempt.id).
        join(Problem,Problem.id==Attempt.problem_id).
        where(Problem.user_id == current_user.id,Attempt.problem_id == problem_id,Note.attempt_id == attempt_id).
        limit(limit).offset(offset)
    ).scalars().all()
    return notes




@router.patch("/notes/{note_id}", response_model=NoteResponse)
def edit_note( attempt_id: int , problem_id: int,note_id: int ,edited_data: NoteEdit, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    note = db.execute(
        select(Note).join(Attempt,Note.attempt_id==Attempt.id).
        join(Problem,Problem.id==Attempt.problem_id).
        where(Problem.user_id == current_user.id,Problem.id == problem_id,Attempt.id == attempt_id,Note.id == note_id)
    ).scalar_one_or_none()
    if note is None:
        raise HTTPException(status_code=404, detail="note  not found")
    if edited_data.content is not None and edited_data.content != note.content :
        note.content = edited_data.content
        note.written_at = datetime.now()
        db.commit()
        db.refresh(note)
    return note




@router.post("/notes", response_model=NoteResponse)
def add_note( attempt_id:int , problem_id: int ,note_data: NoteAdd,db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user)):
    attempt = db.execute(
        select(Attempt).join(Problem,Attempt.problem_id==Problem.id).
        where(Problem.user_id == current_user.id,Attempt.problem_id == problem_id,Attempt.id == attempt_id)
    ).scalar_one_or_none()
    if attempt is None:
        raise HTTPException(status_code=404, detail="attempt not found")

    new_note = Note(
        attempt_id =attempt_id,
        content = note_data.content,
        written_at = datetime.now()
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@router.delete("/notes/{note_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_note(attempt_id: int , problem_id: int,note_id: int , db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    note = db.execute(
        select(Note).join(Attempt,Attempt.id == Note.attempt_id).
        join(Problem,Problem.id == Attempt.problem_id).
        where(Problem.user_id == current_user.id,Problem.id == problem_id,Attempt.id == attempt_id,Note.id == note_id)
    ).scalar_one_or_none()
    if note is None:
        raise HTTPException(status_code=404, detail="note  not found")
    db.delete(note)
    db.commit()


