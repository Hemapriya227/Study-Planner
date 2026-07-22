from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


# ============================================================
# USER SCHEMAS
# ============================================================
class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================
# SUBJECT SCHEMAS
# ============================================================
class SubjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    exam_date: Optional[datetime] = None


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    exam_date: Optional[datetime] = None


class SubjectResponse(SubjectBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================
# TASK/TOPIC SCHEMAS
# ============================================================
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    difficulty: str  # "Easy", "Medium", "Hard"
    estimated_hours: float


class TaskCreate(TaskBase):
    subject_id: int


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    difficulty: Optional[str] = None
    estimated_hours: Optional[float] = None
    status: Optional[str] = None


class TaskResponse(TaskBase):
    id: int
    subject_id: int
    status: str
    completed_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================
# SCHEDULE SCHEMAS
# ============================================================
class ScheduleBase(BaseModel):
    subject_id: int
    task_id: Optional[int] = None
    scheduled_date: datetime
    duration_hours: float
    notes: Optional[str] = None


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleResponse(ScheduleBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================
# USER AVAILABILITY SCHEMAS
# ============================================================
class AvailabilityBase(BaseModel):
    day_of_week: str  # "Monday", "Tuesday", etc.
    available_hours: float


class AvailabilityCreate(AvailabilityBase):
    pass


class AvailabilityResponse(AvailabilityBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================
# AUTH RESPONSE SCHEMA
# ============================================================
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    user_id: int