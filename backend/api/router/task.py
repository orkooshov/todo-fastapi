from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from backend.database import models as m
from backend.services import subtask as subtask_utils, task as task_utils
from backend.api import dependency as dep
from backend.schema import task as s


router = APIRouter(prefix='/task', tags=['task'])

@router.get('/')
async def list_tasks(*, db: Session = Depends(dep.get_db), 
                    user: m.User = Depends(dep.authorize),
                    subtasks: bool = False) -> list[s.RetrieveTaskResponse | s.Task]:
    tasks = task_utils.get_user_tasks(db, user.id)
    schema = s.Task
    if subtasks:
        schema = s.RetrieveTaskResponse
    resp = (schema.model_validate(i) for i in tasks)
    return resp

@router.get('/{task_id}')
async def retrieve_task(*, db: Session = Depends(dep.get_db),
                        user: m.User = Depends(dep.authorize),
                        task_id: int) -> s.RetrieveTaskResponse:
    task = task_utils.get_task(db, user.id, task_id)
    if not task:
        raise HTTPException(404, 'task not found')
    task = s.RetrieveTaskResponse.model_validate(task)
    return task

@router.post('/', status_code=201)
async def create_task(*, db: Session = Depends(dep.get_db),
                      user: m.User = Depends(dep.authorize),
                      body: s.Task) -> s.Task:
    kwargs = body.model_dump()
    kwargs.pop('id')
    task = task_utils.create_task(db, user.id, **kwargs)
    return s.Task.model_validate(task)

@router.patch('/{task_id}')
async def update_task(*, db: Session = Depends(dep.get_db),
                      user: m.User = Depends(dep.authorize),
                      task_id: int,
                      body: s.Task) -> s.Task:
    kwargs = body.model_dump()
    kwargs.pop('id')
    task = task_utils.update_task(db, user.id, task_id, **kwargs)
    if not task:
        raise HTTPException(404, 'task not found')
    return s.Task.model_validate(task)

@router.delete('/{task_id}', status_code=204)
async def delete_task(*, db: Session = Depends(dep.get_db),
                      user: m.User = Depends(dep.authorize),
                      task_id: int) -> None:
    task_utils.delete_task(db, user.id, task_id)
