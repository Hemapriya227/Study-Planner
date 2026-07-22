from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone

from app.database import get_db
from app.models import Task, TaskStatus, Subject
from app.schemas import TaskCreate, TaskResponse, TaskUpdate
from app.middleware.auth_middleware import verify_token


router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    # Verify that the subject exists and belongs to the logged-in user
    subject = db.query(Subject).filter(
        Subject.id == task.subject_id,
        Subject.user_id == user_id
    ).first()

    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )

    db_task = Task(
        user_id=user_id,
        subject_id=task.subject_id,
        title=task.title,
        description=task.description,
        deadline=task.deadline,
        difficulty=task.difficulty,
        estimated_hours=task.estimated_hours,
        status=TaskStatus.PENDING
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    subject_id: Optional[int] = None,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    query = db.query(Task).filter(Task.user_id == user_id)

    if subject_id is not None:
        query = query.filter(Task.subject_id == subject_id)

    return query.all()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    update_data = task_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key == "status" and value == TaskStatus.COMPLETED.value:
            task.completed_at = datetime.now(timezone.utc)

        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return None


@router.patch("/{task_id}/complete", response_model=TaskResponse)
def mark_task_complete(
    task_id: int,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    task.status = TaskStatus.COMPLETED
    task.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(task)

    return task