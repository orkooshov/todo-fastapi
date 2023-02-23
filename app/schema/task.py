from pydantic import BaseModel, Field
from datetime import datetime as dt


class BaseTask(BaseModel):
    id: int | None = None
    title: str
    description: str = ''
    is_done: bool = Field(False, alias='isDone')
    is_favorite: bool = Field(False, alias='isFavorite')
    date_until: dt | None = Field(None, alias='dateUntil')
    created_at: dt | None = Field(None, 'createdAt')
    updated_at: dt | None = Field(None, 'updatedAt')


class Task(BaseTask):
    pass
