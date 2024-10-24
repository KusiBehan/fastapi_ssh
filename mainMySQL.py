from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
# import uvicorn 
from typing import List
import CRUD  # Ensure you have the right import here
from database import SessionLocal
from model import TaskResponse , TaskCreate   # Adjust according to your structure
import bcrypt

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    

# CRUD task

@app.get("/tasks/", response_model=List[TaskResponse])  # Use the Pydantic model for responses
def get_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = CRUD.get_tasks(db, skip=skip, limit=limit)
    return users


@app.get("/tasks/{task_id}/", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    db_task = CRUD.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_task

@app.post("/tasks/", response_model=TaskResponse)
def post_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = CRUD.create_task(db=db, task=task)  
    return new_task 



@app.put('/tasks/{task_id}/', response_model=TaskResponse)
def update_task(task_id: int, task : TaskCreate, db: Session = Depends(get_db)):
    db_task = CRUD.get_task(db, task_id=task_id)
    updated_task = CRUD.update_task(db=db, task_id=task_id, task = task)
    return updated_task