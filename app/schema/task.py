from pydantic import BaseModel
from datetime import datetime as dt


class BaseTask(BaseModel):
    id: int | None = None
    title: str
    description: str = ''
    isDone: bool = False
    isFavorite: bool = False
    dateUntil: dt | None = None

class Task(BaseTask):
    pass
