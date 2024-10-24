# # app/schemas.py
# from pydantic import BaseModel
# from typing import List, Optional

# # User Schema
# class UserBase(BaseModel):
#     email: str
#     name: str

# class UserCreate(UserBase):
#     pass

# class User(UserBase):
#     id: int
#     todos: List['Todo'] = []  # This will hold the user's todos

#     class Config:
#         orm_mode = True

# # Todo Schema
# class TodoBase(BaseModel):
#     title: str
#     description: Optional[str] = None

# class TodoCreate(TodoBase):
#     pass

# class Todo(TodoBase):
#     id: int
#     user_id: int

#     class Config:
#         orm_mode = True
