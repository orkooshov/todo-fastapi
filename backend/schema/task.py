from pydantic import BaseModel
from datetime import datetime as dt
from backend.schema.subtask import Subtask


class BaseTask(BaseModel):
    id: int | None = None
    title: str
    description: str = ''
    is_done: bool = False
    is_favorite: bool = False
    date_until: dt | None = None
    created_at: dt | None = None
    updated_at: dt | None = None

    class Config:
        # populate_by_name = True
        from_attributes = True


class Task(BaseTask):
    pass


class RetrieveTaskResponse(Task):
    subtasks: list[Subtask]