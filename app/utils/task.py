from sqlalchemy.orm import Session
from app.database import models as m


def get_user_tasks(db: Session, user_id: int) -> list[m.Task]:
    return db.query(m.Task).filter(m.Task.user_id == user_id).all()

def get_task(db: Session, user_id: int, task_id: int) -> m.Task | None:
    return (db
        .query(m.Task)
        .filter(m.Task.id == task_id and m.Task.user_id == user_id)
        .first())

def create_task(db: Session, user_id: int, **kwargs) -> m.Task:
    task = m.Task(user_id=user_id, **kwargs)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task(db: Session, user_id: int, task_id: int, **kwargs) -> m.Task | None:
    task = get_task(db, user_id, task_id)
    if not task:
        return None
    task.title = kwargs.get('title', task.title)
    task.description = kwargs.get('description', task.description)
    task.is_done = kwargs.get('is_done', task.is_done)
    task.is_favorite = kwargs.get('is_favorite', task.is_favorite)
    task.date_until = kwargs.get('date_until', task.date_until)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, user_id: int, task_id: int) -> None:
    task = get_task(db, user_id, task_id)
    if task:
        db.delete(task)
