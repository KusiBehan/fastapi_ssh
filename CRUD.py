from sqlalchemy.orm import Session  # Importing Session from SQLAlchemy to manage database transactions
import model  # Importing model to access database models and schemas


# Function to retrieve a list of categories from the database
def get_categories(db: Session, skip: int = 0, limit: int = 100):
    # Query the Category table, apply an offset, limit the results, and retrieve all rows
    return db.query(model.Category).offset(skip).limit(limit).all()


# Function to retrieve a single category by its ID
def get_category(db: Session, category_id: int):
    # Query the Category table and filter by the specified category_id
    # Retrieve the first matching result (or None if not found)
    return db.query(model.Category).filter(model.Category.category_id == category_id).first()


# Function to update a category in the database
def update_category(db: Session, category_id: int, new_category: model.CategoryCreate):
    # Retrieve the existing category entry by category_id
    db_category = get_category(db, category_id)
    
    # Update fields of the category with values from new_category
    for key, value in new_category.model_dump().items():
        setattr(db_category, key, value)  # Set each attribute of db_category to the corresponding new value
    
    db.commit()  # Commit the changes to the database
    db.refresh(db_category)  # Refresh db_category to reflect updated data
    return db_category  # Return the updated category


# Function to retrieve tasks associated with a user from the database
def get_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    # Query the Task table, filter by user_id, apply offset and limit, and retrieve all matching rows
    return db.query(model.Task).filter(model.Task.user_id == user_id).offset(skip).limit(limit).all()


# Function to retrieve a single task by user ID and task ID
def get_task(db: Session, user_id: int, task_id: int):
    # Query the Task table, filter by both task_id and user_id to find the specific task
    return db.query(model.Task).filter(model.Task.task_id == task_id).filter(model.Task.user_id == user_id).first()


# Function to create a new task for a specific user in the database
def create_task(db: Session, user_id: int, task: model.TaskCreate):
    # Create a new Task instance with the provided user_id and other task attributes
    db_Task = model.Task(
        user_id=user_id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        category_id=task.category_id
    ) 
    
    db.add(db_Task)  # Add the new task to the session
    db.commit()  # Commit the transaction to save the new task to the database
    db.refresh(db_Task)  # Refresh the task instance to reflect saved data, including any generated fields
    return db_Task  # Return the newly created task


# Function to update an existing task's details in the database
def update_task(db: Session, user_id: int, task_id: int, new_task: model.TaskPut):
    # Retrieve the existing task entry by user_id and task_id
    db_task = get_task(db, user_id=user_id, task_id=task_id)
    
    # Update fields of the task with values from new_task
    for key, value in new_task.model_dump().items():
        setattr(db_task, key, value)  # Set each attribute of db_task to the new value
    
    db.commit()  # Commit the changes to the database
    db.refresh(db_task)  # Refresh db_task to reflect updated data
    return db_task  # Return the updated task


# Function to delete a task from the database based on user ID and task ID
def delete_task(db: Session, user_id: int, task_id: int):
    # Retrieve the task to delete by user_id and task_id
    tasks = get_task(db, user_id=user_id, task_id=task_id)
    
    db.delete(tasks)  # Delete the retrieved task from the session
    db.commit()  # Commit the transaction to permanently delete the task
    return tasks  # Return the deleted task (or None if task was not found)
