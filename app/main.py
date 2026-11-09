from fastapi import FastAPI
from app.api.tasks import router as tasks_router


app = FastAPI()
app.include_router(tasks_router)


@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.get("/about")
def read_about():
    return {
            "project": "Task Manager",
            "description": "My first FastAPI project"
            }

