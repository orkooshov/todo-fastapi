from pydantic import BaseModel, Field
from datetime import datetime as dt
from app.schema.subtask import Subtask


class BaseTask(BaseModel):
    id: int | None = None
    title: str
    description: str = ''
    is_done: bool = Field(False, alias='isDone')
    is_favorite: bool = Field(False, alias='isFavorite')
    date_until: dt | None = Field(None, alias='dateUntil')
    created_at: dt | None = Field(None, alias='createdAt')
    updated_at: dt | None = Field(None, alias='updatedAt')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Task(BaseTask):
    pass


class RetrieveTaskResponse(Task):
    subtasks: list[Subtask]