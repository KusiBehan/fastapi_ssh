from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uvicorn
import CRUD 
from database import SessionLocal
from model import TaskResponse , TaskCreate, CategoryResponse

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
    
@app.get("/tasks/", response_model=List[TaskResponse]) 
def get_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = CRUD.get_tasks(db, skip=skip, limit=limit)
    return users


@app.get("/tasks/{task_id}/", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    db_task = CRUD.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
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

@app.delete("/tasks/{task_id}/", response_model=TaskResponse)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return CRUD.delete_task(db,task_id=task_id) 


@app.get('/categories/', response_model=List[CategoryResponse])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return CRUD.get_categories(db,skip=skip,limit=limit)

# uvicorn mainMySQL:app --host 10.3.32.18 --port 8000


if __name__ == "__main__":
    uvicorn.run(app, host="10.3.32.18", port=8000)

