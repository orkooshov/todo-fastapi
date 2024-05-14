from pydantic import BaseModel, Field


class BaseSubtask(BaseModel):
    id: int | None = None
    title: str
    is_done: bool = Field(False, alias='isDone')
    task_id: int = Field(alias='taskId')

    class Config:
        populate_by_name = True
        from_attributes = True


class Subtask(BaseSubtask):
    pass
