from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
timezone
import enum

Base = declarative_base()

# ============================================================
# USER MODEL
# ============================================================
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda:datetime.now(timezone.utc))
    
    # Relationships
    subjects = relationship("Subject", back_populates="owner", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")
    schedules = relationship("Schedule", back_populates="owner", cascade="all, delete-orphan")


# ============================================================
# SUBJECT MODEL
# ============================================================
class Subject(Base):
    __tablename__ = "subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)  # e.g., "DSP", "Communication Systems"
    exam_date = Column(DateTime, nullable=True)  # Optional exam date
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    owner = relationship("User", back_populates="subjects")
    tasks = relationship("Task", back_populates="subject", cascade="all, delete-orphan")
    schedules = relationship("Schedule", back_populates="subject", cascade="all, delete-orphan")


# ============================================================
# TASK/TOPIC MODEL
# ============================================================
class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    title = Column(String, nullable=False)  # e.g., "PCM Concepts"
    description = Column(Text, nullable=True)
    deadline = Column(DateTime, nullable=True)
    difficulty = Column(String, nullable=False)  # "Easy", "Medium", "Hard"
    estimated_hours = Column(Float, nullable=False)  # e.g., 2.5 hours
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    owner = relationship("User", back_populates="tasks")
    subject = relationship("Subject", back_populates="tasks")


# ============================================================
# SCHEDULE MODEL (Generated schedule entries)
# ============================================================
class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    scheduled_date = Column(DateTime, nullable=False)
    duration_hours = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    owner = relationship("User", back_populates="schedules")
    subject = relationship("Subject", back_populates="schedules")


# ============================================================
# USER AVAILABILITY MODEL (When user is available)
# ============================================================
class UserAvailability(Base):
    __tablename__ = "user_availability"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    day_of_week = Column(String, nullable=False)  # "Monday", "Tuesday", etc.
    available_hours = Column(Float, nullable=False)  # e.g., 2.0, 3.5
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))