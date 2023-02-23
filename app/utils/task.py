from sqlalchemy.orm import Session
from app.database.models import Task


def get_user_tasks(db: Session, user_id: int) -> list[Task]:
    return db.query(Task).filter(Task.user_id == user_id).all()

def get_task(db: Session, user_id: int, task_id: int) -> Task | None:
    return (db
        .query(Task)
        .filter(Task.id == task_id and Task.user_id == user_id)
        .first())

# def create_task(db: Session, )