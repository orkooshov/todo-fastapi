from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.utils import dependency as dep, subtask as subtask_utils
from backend.database import models as m
from backend.schema.subtask import Subtask


router = APIRouter(prefix='/subtask', tags=['subtask'])

@router.post('/')
async def create_subtask(*, db: Session = Depends(dep.get_db), 
                         user: m.User = Depends(dep.authorize),
                         body: Subtask) -> Subtask | None:
    kwargs = body.model_dump()
    kwargs.pop('id')
    subtask = subtask_utils.insert_subtask(db, user.id, **kwargs)
    if subtask:
        return Subtask.model_validate(subtask)
    raise HTTPException(400, f'task with id {body.task_id} not found')

@router.delete('/{subtask_id}', status_code=204)
async def delete_subtask(*, db: Session = Depends(dep.get_db), 
                       user: m.User = Depends(dep.authorize),
                       subtask_id: int) -> None:
    if not subtask_utils.delete_subtask(db, user.id, subtask_id):
        raise HTTPException(404, f'subtask with id {subtask_id} not found')
