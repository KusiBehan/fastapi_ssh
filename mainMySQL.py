from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uvicorn
import CRUD 
from database import SessionLocal
from model import TaskResponse , TaskCreate, CategoryResponse, CategoryCreate, TaskPut
from auth import verify_token
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Tasks sichtbar 

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
# Task Mehods
@app.get("/tasks/", response_model=List[TaskResponse]) 
def get_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    users = CRUD.get_tasks(db, user_id, skip=skip, limit=limit)
    return users


@app.get("/tasks/{task_id}/", response_model=TaskResponse,)
def get_task(task_id: int, db: Session = Depends(get_db),user_id: int = Depends(verify_token)):
    db_task = CRUD.get_task(db, user_id, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.post("/tasks/", response_model=TaskResponse)
def post_task(task: TaskCreate, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    new_task = CRUD.create_task(db=db, user_id= user_id, task=task, )  
    return new_task 

@app.put('/tasks/{task_id}/', response_model=TaskResponse)
def update_task(task_id: int, task : TaskPut, db: Session = Depends(get_db),user_id: int = Depends(verify_token)):
    updated_task = CRUD.update_task(db=db, task_id=task_id, new_task = task)
    return updated_task

@app.delete("/tasks/{task_id}/", response_model=TaskResponse)
def delete_task(task_id: int, db: Session = Depends(get_db),user_id: int = Depends(verify_token)):
    return CRUD.delete_task(db,task_id=task_id) 


#Categories Endpoint
@app.get('/categories/', response_model=List[CategoryResponse])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    return CRUD.get_categories(db,skip=skip,limit=limit)

@app.get("/categories/{category_id}/", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    db_category = CRUD.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@app.put('/categories/{category_id}/', response_model=CategoryResponse, dependencies=[Depends(verify_token)])
def update_category(category_id: int, category : CategoryCreate, db: Session = Depends(get_db)):
    # db_category = CRUD.get_category(db, category_id = category_id)
    updated_category = CRUD.update_category(db=db, category_id=category_id, new_category=category)
    return updated_category

if __name__ == "__main__":
    uvicorn.run(app, host="10.3.32.18", port=8000)  