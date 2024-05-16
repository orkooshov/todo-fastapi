from sqlalchemy.orm import Session
from backend.database import models as m
from backend.services import task as task_utils


def belongs_to_user(user_id: int, subtask: m.Subtask) -> bool:
    return user_id == subtask.task.user_id

def get_subtask_by_id(db: Session, user_id: int, subtask_id: int) -> m.Subtask | None:
    subtask = db.query(m.Subtask).filter(m.Subtask.id == subtask_id).first()
    if subtask and belongs_to_user(user_id, subtask):
        return subtask

def insert_subtask(db: Session, user_id: int, **kwargs) -> m.Subtask | None:
    task = task_utils.get_task(db, user_id, kwargs['task_id'])
    if task: # if task belongs to user
        subtask = m.Subtask(**kwargs)
        db.add(subtask)
        db.commit()
        db.refresh(subtask)
        return subtask

def delete_subtask(db: Session, user_id: int, subtask_id: int) -> bool:
    subtask = get_subtask_by_id(db, user_id, subtask_id)
    if not subtask:
        return False
    db.delete(subtask)
    db.commit()
    return True
