from sqlalchemy.orm import Session
import model
import bcrypt

# CRUD for tasks

def get_tasks(db:Session, skip: int = 0, limit: int = 100):
    return db.query(model.Task).offset(skip).limit(limit).all()

def get_task(db:Session, task_id: int):
    return db.query(model.Task).filter(model.Task.task_id == task_id).first()

def create_task(db: Session, task : model.TaskCreate):
    db_Task = model.Task(
        user_id = task.user_id,
        title = task.title,
        description = task.description,
        due_date = task.due_date
    ) 
    
    db.add(db_Task)
    db.commit()
    db.refresh(db_Task)
    return db_Task


def update_task(db: Session, task_id: int, task: model.TaskCreate):
    db_task = get_task(db, task_id=task_id)
    db_task = task
    
    db.commit()
    db.refresh(db_task)
    return db_task
    
    

# def create_user_todo(db: Session, user_id: int, todo: schemas.TodoCreate):
#     db_todo = models.Todo(**todo.dict(), user_id=user_id)
#     db.add(db_todo)
#     db.commit()
#     db.refresh(db_todo)
#     return db_todo

# def get_todos(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Todo).offset(skip).limit(limit).all()

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')    