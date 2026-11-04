from fastapi import FastAPI
from app.models.task import TaskCreate, Task

app = FastAPI()
tasks = []
id_counter = 1

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.get("/about")
def read_about():
    return {
            "project": "Task Manager",
            "description": "My first FastAPI project"
            }

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(task: TaskCreate):
    global id_counter
    new_task = Task(id=id_counter, title=task.title, description=task.description)
    tasks.append(new_task)
    id_counter += 1
    return new_task
    