from pydantic import BaseModel, ConfigDict
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    description: str


class Task(TaskCreate):
    id: int
    is_completed: bool = False

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None