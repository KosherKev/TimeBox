from fastapi import HTTPException
from sqlalchemy import between, and_
from sqlalchemy.orm import Session
from .models import User, Task, TimePeriod, TaskAssignment
from .schemas import UserCreate, TaskCreate, TaskUpdate
# from datetime import datetime, timedelta

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
            raise HTTPException(status_code=403, detail="Cannot create more than 3 top task")
        else:
            db_task = Task(task_name=task.task_name, task_description=task.task_description, priority=task.priority)
            db.add(db_task)
            db.commit()
            db.refresh(db_task)
            return db_task
    else:
        db_task = Task(task_name=task.task_name, task_description=task.task_description, priority=task.priority)
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
        db.query(TimePeriod).filter(TimePeriod.assignment_id == task_to_delete.assignment_id).update({TimePeriod.assignment_id: None})
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

def get_unassigned_time_periods(db: Session):
    return db.query(TimePeriod).filter(TimePeriod.assignment_id.is_(None)).all()

def get_unassigned_tasks(db: Session):
    return db.query(Task.task_id, Task.task_name).filter(Task.assignment_id.is_(None)).all()

def create_and_assign_task_assignment(db: Session, task_id: int, time_period_id: int):
    task_assignment = TaskAssignment(task_id=task_id, task_period_id=time_period_id)
    db.add(task_assignment)
    db.commit()
    db.refresh(task_assignment)
    
    task = db.query(Task).filter(Task.task_id == task_id).first()
    time_period = db.query(TimePeriod).filter(TimePeriod.id == time_period_id).first()
    
    if task and time_period:
        task.assignment_id = task_assignment.id
        time_period.assignment_id = task_assignment.id
        
        db.commit()
        db.refresh(task)
        db.refresh(time_period)
    
    return task_assignment

def get_tasks_and_time(db: Session):
    results = db.query(Task.task_name, TaskAssignment.id, TimePeriod.start_time)\
                .join(TaskAssignment, Task.assignment_id == TaskAssignment.id)\
                .join(TimePeriod, TaskAssignment.task_period_id == TimePeriod.id)\
                .filter(Task.assignment_id.isnot(None))\
                .order_by(TimePeriod.start_time)\
                .all()
    return [{"task_name": task_name, "assignment_id": id, "start_time": start_time} for task_name, id, start_time in results]

def unassign_task_and_time_period_by_assignment_id(db: Session, task_assignment_id: int):
    task_assignment = db.query(TaskAssignment).filter(TaskAssignment.id == task_assignment_id).first()

    if not task_assignment:
        return {"message": "Task assignment not found."}

    task = db.query(Task).filter(Task.assignment_id == task_assignment_id).first()
    time_period = db.query(TimePeriod).filter(TimePeriod.assignment_id == task_assignment_id).first()

    if task:
        task.assignment_id = None
    else:
        return {"message": "Task not found or already unassigned."}

    if time_period:
        time_period.assignment_id = None
    else:
        return {"message": "Time period not found or already unassigned."}

    db.delete(task_assignment)
    db.commit()

    return {"message": "Task and time period unassigned successfully"}