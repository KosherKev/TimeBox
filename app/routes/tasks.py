from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.TaskCreate)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    return crud.create_task(db=db, task=task)

@router.get("get/<task_id>", response_model=schemas.TaskCreate)
def read_task(task_id: int, db: Session = Depends(database.get_db)):
    db_task = crud.get_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

<<<<<<< HEAD
@router.get("/top/tasks", response_model= List[schemas.Task])
=======
@router.get("/top", response_model= List[schemas.Task])
>>>>>>> c111368b18fc74f9bfbb08553d93c1f82f11df83
def list_top_tasks(db: Session = Depends(database.get_db)):
    tasks = crud.get_top_tasks(db)
    return tasks

@router.delete("/remove/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    return crud.delete_task(db=db, task_id=task_id)

@router.get("/secondary", response_model=List[schemas.Task])
def read_secondary_tasks(db: Session = Depends(database.get_db)):
    return crud.get_secondary_tasks(db)

@router.get("/all", response_model=List[schemas.Task])
def read_all_tasks(db: Session = Depends(database.get_db)):
    return crud.get_all_tasks(db)

@router.put("/update/<task_id>")
def update_task(task_id: int,task_update: schemas.TaskUpdate, db: Session = Depends(database.get_db)):
    return crud.update_task(task_id, task_update, db)