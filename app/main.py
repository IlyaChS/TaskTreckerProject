from fastapi import FastAPI, HTTPException
from app.models.task import TaskCreate, Task
from app.storage import tasks, id_counter


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.get("/about")
def read_about():
    return {
            "project": "Task Manager",
            "description": "My first FastAPI project"
            }



@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/tasks")
def create_task(task: TaskCreate):
    global id_counter
    new_task = Task(id=id_counter, title=task.title, description=task.description)
    tasks.append(new_task)
    id_counter += 1
    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskCreate):
    for task in tasks:
        if task.id == task_id:
            task.title = updated_task.title
            task.description = updated_task.description
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")