from fastapi import HTTPException
from sqlalchemy.orm import Session
from .models import User, Task
from .schemas import UserCreate, TaskCreate

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
    return db.query(Task).filter(Task.priority == "S").all()

def get_all_tasks(db: Session):
    return db.query(Task).all()
