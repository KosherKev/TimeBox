from sqlalchemy import Column, Integer, String, DateTime, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
import enum

class PriorityEnum(enum.Enum):
    P = "P"
    S = "S"

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(255), nullable=False)
    user_email = Column(String(255), nullable=False)
    user_password = Column(String(100), nullable=False)
    tasks = relationship("Task", back_populates="user")

class Task(Base):
    __tablename__ = 'tasks'
    task_id = Column(Integer, primary_key=True)
    task_name = Column(String(100), nullable=False)
    task_description = Column(String(255))
    startT = Column(DateTime)
    endT = Column(DateTime)
    priority = Column(Enum(PriorityEnum))
    created_on = Column(TIMESTAMP)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship("User", back_populates="tasks")
