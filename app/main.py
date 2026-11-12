from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.api.tasks import router as tasks_router
from app.database.db import Base, engine
from app.models.task import Task
from app.logging_config import logger


app = FastAPI()
app.include_router(tasks_router)
Base.metadata.create_all(bind=engine)

logger.info("Application has started.")


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(
    request: Request,
    exc: SQLAlchemyError
):
    logger.error(
        "Database error: %s",
        exc,
        exc_info=True
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error"}
    )


@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.get("/about")
def read_about():
    return {
            "project": "Task Manager",
            "description": "My first FastAPI project"
            }

