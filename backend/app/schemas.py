from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ----------- USERS -----------

class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    user_id: int
    class Config:
        orm_mode = True


# ----------- TOKENS -----------

class TokenBase(BaseModel):
    token: str
    expire_date: datetime

class TokenCreate(TokenBase):
    user_id: int

class TokenOut(TokenBase):
    token_id: int
    user_id: int
    class Config:
        orm_mode = True


# ----------- TASKS -----------

class TaskBase(BaseModel):
    title: str
    description: Optional[str]
    state: str
    due_date: Optional[datetime]

class TaskCreate(TaskBase):
    user_id: int

class TaskOut(TaskBase):
    task_id: int
    creation_date: datetime
    class Config:
        orm_mode = True


# ----------- TASK HISTORY -----------

class TaskHistoryBase(BaseModel):
    last_state: str
    actual_state: str
    change_date: Optional[datetime]

class TaskHistoryCreate(TaskHistoryBase):
    task_id: int

class TaskHistoryOut(TaskHistoryBase):
    history_id: int
    task_id: int
    class Config:
        orm_mode = True
