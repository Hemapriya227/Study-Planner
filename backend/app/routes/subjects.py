from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Subject
from app.schemas import SubjectCreate, SubjectResponse, SubjectUpdate
from app.middleware.auth_middleware import verify_token

router = APIRouter(prefix="/api/subjects", tags=["subjects"])


@router.post("/", response_model=SubjectResponse)
def create_subject(
    subject: SubjectCreate,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """
    Create a new subject.
    
    Example request:
    {
      "name": "Communication Systems",
      "description": "Prepare for final exam",
      "exam_date": "2026-08-20T00:00:00"
    }
    """
    db_subject = Subject(
        user_id=user_id,
        name=subject.name,
        description=subject.description,
        exam_date=subject.exam_date
    )
    
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    
    return db_subject


@router.get("/", response_model=List[SubjectResponse])
def get_subjects(
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """
    Get all subjects for authenticated user.
    """
    subjects = db.query(Subject).filter(Subject.user_id == user_id).all()
    return subjects


@router.get("/{subject_id}", response_model=SubjectResponse)
def get_subject(
    subject_id: int,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """
    Get a specific subject by ID.
    """
    subject = db.query(Subject).filter(
        Subject.id == subject_id,
        Subject.user_id == user_id
    ).first()
    
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    return subject


@router.put("/{subject_id}", response_model=SubjectResponse)
def update_subject(
    subject_id: int,
    subject_update: SubjectUpdate,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """
    Update a subject.
    """
    subject = db.query(Subject).filter(
        Subject.id == subject_id,
        Subject.user_id == user_id
    ).first()
    
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    # Update only provided fields
    update_data = subject_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(subject, key, value)
    
    db.commit()
    db.refresh(subject)
    
    return subject


@router.delete("/{subject_id}", status_code=204)
def delete_subject(
    subject_id: int,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """
    Delete a subject and all its tasks.
    """
    subject = db.query(Subject).filter(
        Subject.id == subject_id,
        Subject.user_id == user_id
    ).first()
    
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    db.delete(subject)
    db.commit()
    
    return None