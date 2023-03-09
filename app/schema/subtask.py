from pydantic import BaseModel, Field


class BaseSubtask(BaseModel):
    id: int | None = None
    title: str
    is_done: bool = Field(False, alias='isDone')
    task_id: int = Field(alias='taskId')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Subtask(BaseSubtask):
    pass
