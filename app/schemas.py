from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time
from enum import Enum

class PriorityEnum(str, Enum):
    P = "P"
    S = "S"

class UserCreate(BaseModel):
    user_name: str
    user_email: str
    user_password: str
class User(BaseModel):
    user_id: int
    user_name: str
    user_email: str

    class Config:
        from_attributes = True

class TaskAssignmentCreate(BaseModel):
    task_id: int
    task_period_id: int

class TaskAssignment(BaseModel):
    id: int
    task_id: int
    task_period_id: int

    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    task_name: str
    task_description: Optional[str] = None
    priority: PriorityEnum
    assignment_id: Optional[int] = None

class Task(BaseModel):
    task_id: int
    task_name: str
    task_description: str
    priority: PriorityEnum
    created_on: datetime
    updated_on: Optional[datetime]
    assignment_id: Optional[int] = None

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    task_name: Optional[str] = None
    task_description: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    assignment_id: Optional[int] = None

    class Config:
        from_attributes = True

class TimePeriodCreate(BaseModel):
    start_time: time
    assignment_id: Optional[int] = None

class TimePeriod(BaseModel):
    id: int
    start_time: time
    assignment_id: Optional[int] = None

    class Config:
        from_attributes = True