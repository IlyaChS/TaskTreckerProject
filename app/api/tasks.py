from fastapi import APIRouter, HTTPException, Depends
from app import storage
from app.schemas.task import TaskCreate, Task, TaskUpdate


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


def get_task_count():
    return len(storage.tasks)


def get_task_id(task_id: int):
    for task in storage.tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


def check_task_status(task: Task = Depends(get_task_id)):
    if task.is_completed:
        raise HTTPException(status_code=400, detail="Task is already completed")
    return task


@router.get("/", response_model=list[Task], status_code=200)
def get_tasks():
    return storage.tasks


@router.get("/count", status_code=200)
def get_tasks_amount(amount: int = Depends(get_task_count)):
    return {"count": amount}


@router.get("/{task_id}", response_model=Task, status_code=200)
def get_task(task: Task = Depends(get_task_id)):
    return task


@router.post("/", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    new_task = Task(id=storage.id_counter, title=task.title, description=task.description)
    storage.tasks.append(new_task)
    storage.id_counter += 1
    return new_task


@router.put("/{task_id}", response_model=Task, status_code=200)
def update_task(updated_task: TaskCreate, task: Task = Depends(check_task_status)):
    task.title = updated_task.title
    task.description = updated_task.description
    return task


@router.delete("/{task_id}", status_code=200)
def delete_task(task: Task = Depends(get_task_id)):
    if not task.is_completed:
        raise HTTPException(status_code=400, detail="Cannot delete an incomplete task")
    storage.tasks.remove(task)
    return {"message": "Task deleted successfully"}


@router.patch("/{task_id}", response_model=Task, status_code=200)
def patch_task(updated_task: TaskUpdate, task: Task = Depends(check_task_status)):
        update_data = updated_task.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields provided for update")
        for key, value in update_data.items():
            setattr(task, key, value)
        return task



