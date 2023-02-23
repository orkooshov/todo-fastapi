from pydantic import BaseModel, Field


class BaseSubtask(BaseModel):
    id: int | None = None
    title: str
    is_done: bool = Field(False, alias='isDone')
    task_id: int = Field(alias='taskId')


class Subtask(BaseSubtask):
    pass
