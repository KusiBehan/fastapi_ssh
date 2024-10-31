from sqlalchemy.orm import Session
import model


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Category).offset(skip).limit(limit).all()

def get_category(db:Session, category_id: int):
    return db.query(model.Category).filter(model.Category.category_id == category_id).first()

def update_category(db:Session, category_id: int, new_category: model.CategoryCreate):
    db_category = get_category(db, category_id)
    
    for key, value in new_category.model_dump().items():
        setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

def get_tasks(db:Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(model.Task).filter(model.Task.user_id == user_id).offset(skip).limit(limit).all()

def get_task(db:Session, user_id: int, task_id: int):
    return db.query(model.Task).filter(model.Task.task_id == task_id).filter(model.Task.user_id == user_id).first()

def create_task(db: Session, user_id: int, task : model.TaskCreate):
    db_Task = model.Task(
        user_id = user_id,
        title = task.title,
        description = task.description,
        due_date = task.due_date,
        category_id = task.category_id
    ) 
    
    db.add(db_Task)
    db.commit()
    db.refresh(db_Task)
    return db_Task


def update_task(db: Session, user_id: int, task_id: int, new_task: model.TaskPut):
    db_task = get_task(db, user_id=user_id, task_id=task_id)
    
    for key, value in new_task.model_dump().items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task
    

def delete_task(db: Session, user_id : int, task_id: int):
    # tsdk = get_task(db, task_id=task_id)
    tasks = get_task(db, user_id=user_id,task_id=task_id)
    db.delete(tasks)
    db.commit()
    return tasks



###Doku important

# Looks like the new_category parameter in update_category might be an instance of a Pydantic model (e.g., CategoryCreate) used for request validation and not an instance of a SQLAlchemy model. This would explain the error you’re encountering since SQLAlchemy wouldn’t recognize CategoryCreate as a mapped model.

# Here’s how you can fix the code to correctly update an existing SQLAlchemy Category model instance:

# Modify update_category to ensure it assigns each attribute from new_category individually.
# Check CategoryCreate to ensure it’s a Pydantic model with the required fields.
# Here’s the corrected code:

# def update_category(db: Session, category_id: int, new_category: model.CategoryCreate):
#     db_category = get_category(db, category_id)
#     if not db_category:
#         return None  # or raise an exception if the category isn't found
    
#     # Update each field manually
#     for key, value in new_category.dict().items():
#         setattr(db_category, key, value)
    
#     db.commit()
#     db.refresh(db_category)
#     return db_category
# Explanation:
# The code iterates over each field in new_category (a CategoryCreate instance) and sets it on the existing db_category object.
# new_category.dict() converts the Pydantic model to a dictionary, making it easier to handle attribute assignments.
# After setting attributes, db.commit() saves the changes, and db.refresh() reloads the updated object from the database.
# This should solve the issue by ensuring that the existing SQLAlchemy Category model instance is properly updated with the data from CategoryCreate.