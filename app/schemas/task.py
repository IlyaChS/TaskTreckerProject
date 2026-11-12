from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=5, max_length=1000)


class Task(TaskCreate):
    id: int
    is_completed: bool = False

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(min_length=3, max_length=200, default=None)
    description: Optional[str] = Field(min_length=5, max_length=1000, default=None)
    is_completed: Optional[bool] = Field(default=None)