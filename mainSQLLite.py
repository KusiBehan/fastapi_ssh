from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import CRUD  # Ensure you have the right import here
from model import UserResponse, UserCreate, TaskResponse , TaskCreate   # Adjust according to your structure
# from models import Item
from sqlLitedatabase import SessionLocal, init_db

app = FastAPI()

init_db()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post("/users/", response_model=UserResponse)
def post_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user with the same email already exists
    db_user = CRUD.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create the user in the database
    new_user = CRUD.create_user(db=db, user=user)  # Pass the UserCreate instance directly
    return new_user  # Return the created user using the UserResponse model
    return new_user  # This will return the created user using the UserResponse Pydantic model

@app.get("/users/", response_model=List[UserResponse])  # Use the Pydantic model for responses
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = CRUD.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{id}/", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = CRUD.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# CRUD task

@app.get("/tasks/", response_model=List[TaskResponse])  # Use the Pydantic model for responses
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
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
    # Create the task in the database
    new_task = CRUD.create_task(db=db, task=task)  # Pass the UserCreate instance directly
    return new_task # Return the created user using the UserResponse model    



@app.put('/tasks/{task_id}/', response_model=TaskResponse)
def update_task(task_id: int, task : TaskCreate, db: Session = Depends(get_db)):
    db_task = CRUD.get_task(db, task_id=task_id)
    updated_task = CRUD.update_task(db=db, task_id=task_id, task = task)
    return updated_task
    


# uvicorn.run(app, host="0.0.0.0", port=8080)