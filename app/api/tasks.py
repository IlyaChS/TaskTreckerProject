from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.repositories import task_repo
from app.schemas.task import TaskCreate, Task, TaskUpdate


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.get("/", response_model=list[Task], status_code=200)
def get_tasks(db: Session = Depends(get_db)):
    return task_repo.get_all_tasks(db)


@router.get("/count", status_code=200)
def get_tasks_amount(db: Session = Depends(get_db)):
    return {"count": task_repo.get_task_count(db)}


@router.get("/{task_id}", response_model=Task, status_code=200)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = task_repo.get_task_by_id(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/", response_model=Task, status_code=201)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    return task_repo.create_task(db, task_data)


@router.put("/{task_id}", response_model=Task, status_code=200)
def update_task(task_id: int, updated_task: TaskCreate, db: Session = Depends(get_db)):
    task = task_repo.get_task_by_id(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.is_completed:
        raise HTTPException(status_code=400, detail="Cannot update a completed task")
    return task_repo.update_task(db, task, updated_task.model_dump(exclude_unset=True))


@router.delete("/{task_id}", status_code=200)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = task_repo.get_task_by_id(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if not task.is_completed:
        raise HTTPException(status_code=400, detail="Cannot delete an incomplete task")
    task_repo.delete_task(db, task)
    return {"message": "Task deleted successfully"}


@router.patch("/{task_id}", response_model=Task, status_code=200)
def patch_task(task_id: int, updated_task: TaskUpdate, db: Session = Depends(get_db)):
    task = task_repo.get_task_by_id(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.is_completed:
        raise HTTPException(status_code=400, detail="Cannot update a completed task")
    update_data = updated_task.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    return task_repo.update_task(db, task, update_data)

