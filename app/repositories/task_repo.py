from sqlalchemy.orm import Session
from app.models.task import Task


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
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def update_task(db: Session, task: Task, update_data: dict):
    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()
    return True