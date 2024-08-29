from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .. import crud, schemas, database
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.TaskCreate)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    return crud.create_task(db=db, task=task)

# @router.get("/<task_id>", response_model=schemas.TaskCreate)
# @router.get("get/<task_id>", response_model=schemas.TaskCreate)
# def read_task(task_id: int, db: Session = Depends(database.get_db)):
#     db_task = crud.get_task(db=db, task_id=task_id)
#     if db_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return db_task

@router.get("/top", response_model= List[schemas.Task])
def list_top_tasks(db: Session = Depends(database.get_db)):
    tasks = crud.get_top_tasks(db)
    return tasks

@router.delete("/remove/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    return crud.delete_task(db=db, task_id=task_id)

@router.put("/update/{task_id}")
def update_task(task_id: int,task_update: schemas.TaskUpdate, db: Session = Depends(database.get_db)):
    return crud.update_task(task_id, task_update, db)

@router.get("/secondary", response_model=List[schemas.Task])
def read_secondary_tasks(db: Session = Depends(database.get_db)):
    return crud.get_secondary_tasks(db=db)

@router.get("/assigned_time_periods/", response_model=List[schemas.TimePeriod])
def read_assigned_time_periods(db: Session = Depends(database.get_db)):
    assigned_time_periods = crud.get_unassigned_time_periods(db)
    if not assigned_time_periods:
        raise HTTPException(status_code=404, detail="No assigned time periods found")
    return assigned_time_periods

@router.get("/assigned_tasks/", response_model=List[schemas.TaskName])
def read_assigned_tasks(db: Session = Depends(database.get_db)):
    assigned_tasks = crud.get_unassigned_tasks(db)
    if not assigned_tasks:
        raise HTTPException(status_code=404, detail="No assigned tasks found")
    return assigned_tasks
# @router.get("/tasks_near_time")
# def tasks_near_time(db: Session = Depends(database.get_db)):
#     tasks = crud.get_tasks_near_time(db, datetime.now())
#     return tasks
