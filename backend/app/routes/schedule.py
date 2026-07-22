from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta, timezone

from app.database import get_db
from app.models import Schedule, Task, TaskStatus
from app.schemas import ScheduleResponse
from app.middleware.auth_middleware import verify_token


router = APIRouter(prefix="/api/schedule", tags=["schedule"])


@router.get("/", response_model=List[ScheduleResponse])
def get_schedule(
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    schedules = db.query(Schedule).filter(
        Schedule.user_id == user_id
    ).all()

    return schedules


@router.get("/week", response_model=List[ScheduleResponse])
def get_weekly_schedule(
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    today = datetime.now(timezone.utc)

    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=7)

    schedules = db.query(Schedule).filter(
        Schedule.user_id == user_id,
        Schedule.scheduled_date >= week_start,
        Schedule.scheduled_date < week_end
    ).all()

    return schedules


@router.post("/generate")
def generate_schedule(
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    # Get pending tasks belonging to the logged-in user
    pending_tasks = (
        db.query(Task)
        .filter(
            Task.user_id == user_id,
            Task.status == TaskStatus.PENDING
        )
        .order_by(
            Task.deadline.asc(),
            Task.difficulty.desc()
        )
        .all()
    )

    if not pending_tasks:
        return {
            "message": "No pending tasks to schedule",
            "schedules_created": 0
        }

    # Remove old schedule before generating a new one
    db.query(Schedule).filter(
        Schedule.user_id == user_id
    ).delete(synchronize_session=False)

    schedules_created = 0
    start_date = datetime.now(timezone.utc)

    # Simple temporary scheduling algorithm
    for index, task in enumerate(pending_tasks):

        scheduled_date = start_date + timedelta(
            days=index % 7
        )

        schedule = Schedule(
            user_id=user_id,
            subject_id=task.subject_id,
            task_id=task.id,
            scheduled_date=scheduled_date,
            duration_hours=task.estimated_hours,
            notes=f"Study {task.title}"
        )

        db.add(schedule)
        schedules_created += 1

    db.commit()

    return {
        "message": (
            f"Schedule generated with "
            f"{schedules_created} entries"
        ),
        "schedules_created": schedules_created
    }


@router.delete("/clear")
def clear_schedule(
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db)
):
    db.query(Schedule).filter(
        Schedule.user_id == user_id
    ).delete(synchronize_session=False)

    db.commit()

    return {"message": "Schedule cleared"}