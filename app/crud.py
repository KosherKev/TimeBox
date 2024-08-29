from fastapi import HTTPException
from sqlalchemy import between, and_
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .models import User, Task, TimePeriod
from .schemas import UserCreate, TaskCreate, TaskUpdate

def create_user(db: Session, user: UserCreate):
    db_user = User(user_name=user.user_name, user_email=user.user_email, user_password=user.user_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

def create_task(db: Session, task: TaskCreate):
    if task.priority == 'P': 
        if len(get_top_tasks(db)) >= 3:
            raise HTTPException(status_code=400, detail="Cannot create more than 3 top task")
        else:
            db_task = Task(task_name=task.task_name, task_description=task.task_description, startT=task.startT, endT=task.endT, priority=task.priority)
            db.add(db_task)
            db.commit()
            db.refresh(db_task)
            return db_task
    else:
        db_task = Task(task_name=task.task_name, task_description=task.task_description, startT=task.startT, endT=task.endT, priority=task.priority)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.task_id == task_id).first()

def get_top_tasks(db: Session):
    return db.query(Task).filter(Task.priority == 'P').all()

def delete_task(db: Session, task_id: int):
    task_to_delete = db.query(Task).filter(Task.task_id == task_id).first()
    if task_to_delete:
        db.delete(task_to_delete)
        db.commit()
        return task_to_delete
    else:
        raise HTTPException(status_code=404, detail="Task not found")

def get_secondary_tasks(db: Session):
    return db.query(Task).filter(Task.priority == 'S').all()

def get_all_tasks(db: Session):
    return db.query(Task).all()

def update_task(task_id: int, task_update: TaskUpdate, db: Session):
    task_to_update = db.query(Task).filter(Task.task_id == task_id).first()
    if not task_to_update:
        raise HTTPException(detail="Task not found")  
    for key, value in task_update.model_dump().items():
        setattr(task_to_update, key, value)
    db.commit()

def get_assigned_time_periods(db: Session):
    return db.query(TimePeriod).filter(TimePeriod.assignment_id.isnot(None)).all()


# def get_tasks_near_time(db: Session, current_time: datetime, time_delta: timedelta = timedelta(minutes=30)):
#     start_time_lower_bound = current_time - time_delta
#     start_time_upper_bound = current_time + time_delta
#     end_time_lower_bound = current_time - time_delta
#     end_time_upper_bound = current_time + time_delta

#     tasks = db.query(Task).filter(
#         and_(
#             between(Task.startT, start_time_lower_bound, start_time_upper_bound),
#             between(Task.endT, end_time_lower_bound, end_time_upper_bound)
#         )
#     ).all()

#     for x, obj in tasks:
#         for y in range(obj.len()) - 1:
#             tasks = y.popitem()
#     return tasks