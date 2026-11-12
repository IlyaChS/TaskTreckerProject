from sqlalchemy.orm import Session
from app.models.task import Task
from sqlalchemy.exc import SQLAlchemyError


def get_all_tasks(db: Session):
    return db.query(Task).all()


def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def get_task_count(db: Session):
    return db.query(Task).count()


def create_task(db: Session, task_data):
    new_task = Task(
        title=task_data.title,
        description=task_data.description
    )
    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def update_task(db: Session, task: Task, update_data: dict):
    for key, value in update_data.items():
        setattr(task, key, value)
    try:
        db.commit()
        db.refresh(task)
        return task
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def delete_task(db: Session, task: Task):
    try:
        db.delete(task)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise e