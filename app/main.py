from fastapi import FastAPI
from app.api.tasks import router as tasks_router
from app.database.db import Base, engine
from app.models.task import Task


app = FastAPI()
app.include_router(tasks_router)
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.get("/about")
def read_about():
    return {
            "project": "Task Manager",
            "description": "My first FastAPI project"
            }

