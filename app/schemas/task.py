from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    description: str


class Task(TaskCreate):
    id: int


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None