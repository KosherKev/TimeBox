from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class PriorityEnum(str, Enum):
    P = "P"
    S = "S"

class UserCreate(BaseModel):
    user_name: str
    user_email: str
    user_password: str

class TaskCreate(BaseModel):
    task_name: str
    task_description: Optional[str] = None
    startT: Optional[datetime] = None
    endT: Optional[datetime] = None
    priority: PriorityEnum
    # user_id: int

class Task(BaseModel):
    task_id: int
    task_name: str
    task_description: str
    startT: datetime
    endT: datetime
    priority: str

    class Config:
        orm_mode = True