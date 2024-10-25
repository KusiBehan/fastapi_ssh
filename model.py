from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLAEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum
from sqlalchemy.sql import func

# SQLAlchemy Base
Base = declarative_base()

# Define the Status Enum for Task
class Status(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    
    
class Category(Base):
    __tablename__ = "Category"

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)  # The name of the category
    description = Column(String)  # Optional field for category description


# SQLAlchemy User Model
class User(Base):
    __tablename__ = 'User'
    
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    date_created = Column(DateTime, default=func.now())
    last_login = Column(DateTime, nullable=True)
    tasks = relationship('Task', backref='owner', lazy=True)  # Establishing relationship with Task

# SQLAlchemy Task Model
class Task(Base):
    __tablename__ = "Task"
    
    task_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('User.user_id'), nullable=False)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)
    date_created = Column(DateTime, default=func.now())
    date_completed = Column(DateTime, nullable=True)
    priority = Column(Integer, default=0)
    status = Column(SQLAEnum(Status), nullable=False)  # Correctly using SQLAlchemy Enum
    category_id = Column(Integer, ForeignKey("categories.category_id"))
    
# class Category(Base):
    

        
# Pydantic Task Models
class TaskBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None 
    due_date: Optional[datetime] = None
    

class TaskCreate(TaskBase):
    user_id : int

class TaskResponse(TaskBase):
    task_id: int  # Ensure this is the correct field name
    user_id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    date_created: datetime
    date_completed: Optional[datetime] = None
    priority: int
    category_id: Optional[int] = None

    class Config:
        orm_mode = True  # Allow Pydantic to work with SQLAlchemy models
        
# class TaskResponsePut(TaskBase):        

class CategoryResponse(BaseModel):
    category_id: int
    name: Optional[str]
    description: Optional[str] = None

    class Config:
        orm_mode = True  # Enables compatibility with SQLAlchemy ORM models     