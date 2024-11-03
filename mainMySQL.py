from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
import uvicorn
import CRUD 
from database import SessionLocal
from model import TaskResponse, TaskCreate, CategoryResponse, CategoryCreate, TaskPut
#Activate dev command for dev and test line for testing the app
# from auth import verify_token //dev
from auth_test import verify_token #//test
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

app = FastAPI()

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

# Task Methods with Updated Status Codes
@app.get("/tasks/", response_model=List[TaskResponse], status_code=status.HTTP_200_OK)
def get_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    try:
        users = CRUD.get_tasks(db, user_id, skip=skip, limit=limit)
        return users
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e

@app.get("/tasks/{task_id}/", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_task(task_id: int, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    try:
        db_task = CRUD.get_task(db, user_id, task_id=task_id)
        if db_task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return db_task
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e

@app.post("/tasks/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def post_task(task: TaskCreate, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    try:
        new_task = CRUD.create_task(db=db, user_id=user_id, task=task)  
        return new_task 
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.put('/tasks/{task_id}/', response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(task_id: int, task: TaskPut, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    try:
        updated_task = CRUD.update_task(db=db, task_id=task_id, new_task=task, user_id=user_id)
        if updated_task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return updated_task
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e

@app.delete("/tasks/{task_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    try:
        deleted_task = CRUD.delete_task(db, user_id= user_id, task_id=task_id)
        if deleted_task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return None  # 204 No Content implies an empty response body
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e

@app.get('/categories/', response_model=List[CategoryResponse], status_code=status.HTTP_200_OK)
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    try:
        return CRUD.get_categories(db, skip=skip, limit=limit)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e

@app.get("/categories/{category_id}/", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def get_category(category_id: int, db: Session = Depends(get_db)):
    try:
        db_category = CRUD.get_category(db, category_id=category_id)
        if db_category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return db_category
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e

@app.put('/categories/{category_id}/', response_model=CategoryResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(verify_token)])
def update_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        updated_category = CRUD.update_category(db=db, category_id=category_id, new_category=category)
        if updated_category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return updated_category
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e

if __name__ == "__main__":
    uvicorn.run(app, host="10.3.32.18", port=8000)
