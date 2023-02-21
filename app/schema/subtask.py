from pydantic import BaseModel


class BaseSubtask(BaseModel):
    id: int | None = None
    title: str
    isDone: bool = False
    taskId: int


class Subtask(BaseSubtask):
    pass
