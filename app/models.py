from sqlalchemy import Column, Integer, String, DateTime, Time, Enum, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship
from .database import Base
import enum

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(255), nullable=False)
    user_email = Column(String(255), nullable=False)
    user_password = Column(String(100), nullable=False)
    # tasks = relationship("Task", back_populates="user")

class TaskAssignment(Base):
    __tablename__ = 'task_assignments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('tasks.task_id'))
    task_period_id = Column(Integer, ForeignKey('time_periods.id'))
    task = relationship('Task', foreign_keys=[task_id])
    time_period = relationship('TimePeriod', foreign_keys=[task_period_id])
class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    task_name = Column(String(100), nullable=False)
    task_description = Column(String(255), nullable=False)
    priority = Column(Enum('P', 'S'), nullable=False)
    created_on = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_on = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    assignment_id = Column(Integer, ForeignKey('task_assignments.id'))
    assignment = relationship('TaskAssignment', foreign_keys=[assignment_id])

class TimePeriod(Base):
    __tablename__ = 'time_periods'
    id = Column(Integer, primary_key=True, autoincrement=True)
    start_time = Column(Time)
    assignment_id = Column(Integer, ForeignKey('task_assignments.id'))
    assignment = relationship('TaskAssignment', foreign_keys=[assignment_id])

    # startT = Column(DateTime)
    # endT = Column(DateTime)
    # user_id = Column(Integer, ForeignKey('users.user_id'))
    # user = relationship("User", back_populates="tasks")