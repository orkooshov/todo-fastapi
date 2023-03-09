from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.database import models as m
from app.utils import task as task_utils, dependency as dep, subtask as subtask_utils
from app.schema import task as s


router = APIRouter(prefix='/task', tags=['task'])

@router.get('/')
async def list_tasks(*, db: Session = Depends(dep.get_db), 
                    user: m.User = Depends(dep.authorize),
                    subtasks: bool = False) -> list[s.RetrieveTaskResponse | s.Task]:
    tasks = task_utils.get_user_tasks(db, user.id)
    schema = s.Task
    if subtasks:
        schema = s.RetrieveTaskResponse
    resp = (schema.from_orm(i) for i in tasks)
    return resp

@router.get('/{task_id}')
async def retrieve_task(*, db: Session = Depends(dep.get_db),
                        user: m.User = Depends(dep.authorize),
                        task_id: int) -> s.RetrieveTaskResponse:
    task = task_utils.get_task(db, user.id, task_id)
    if not task:
        raise HTTPException(404, 'task not found')
    task = s.RetrieveTaskResponse.from_orm(task)
    return task

@router.post('/', status_code=201)
async def create_task(*, db: Session = Depends(dep.get_db),
                      user: m.User = Depends(dep.authorize),
                      body: s.Task) -> s.Task:
    kwargs = body.dict()
    kwargs.pop('id')
    task = task_utils.create_task(db, user.id, **kwargs)
    return s.Task.from_orm(task)

@router.patch('/{task_id}')
async def update_task(*, db: Session = Depends(dep.get_db),
                      user: m.User = Depends(dep.authorize),
                      task_id: int,
                      body: s.Task) -> s.Task:
    kwargs = body.dict()
    kwargs.pop('id')
    task = task_utils.update_task(db, user.id, task_id, **kwargs)
    if not task:
        raise HTTPException(404, 'task not found')
    return s.Task.from_orm(task)

@router.delete('/{task_id})', status_code=204)
async def delete_task(*, db: Session = Depends(dep.get_db),
                      user: m.User = Depends(dep.authorize),
                      task_id: int) -> None:
    task_utils.delete_task(db, user.id, task_id)
