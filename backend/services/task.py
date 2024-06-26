from sqlalchemy.orm import Session
from backend.database import models as m


def get_user_tasks(db: Session, user_id: int) -> list[m.Task]:
    return (
        db.query(m.Task).filter(m.Task.user_id == user_id)
        .order_by(m.Task.id).all()
    )


def get_task(db: Session, user_id: int, task_id: int) -> m.Task | None:
    return (db
            .query(m.Task)
            .filter(m.Task.id == task_id, m.Task.user_id == user_id)
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
    # remove empty values
    updates = {key: value for key,
               value in kwargs.items() if value is not None}
    # set attributes
    for key, value in updates.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, user_id: int, task_id: int) -> None:
    task = get_task(db, user_id, task_id)
    if task:
        db.delete(task)
        db.commit()
