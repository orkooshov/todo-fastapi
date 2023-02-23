from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.database import models as m
from app.utils import task as task_utils, dependency as dep
from app.schema import task as s


router = APIRouter(prefix='/task', tags=['task'])

@router.get('/')
async def list_tasks(db: Session = Depends(dep.get_db), 
                    user: m.User = Depends(dep.authorize)) -> list[s.Task]:
    tasks = task_utils.get_user_tasks(db, user.id)
    resp = (s.Task.from_orm(i) for i in tasks)
    return resp

@router.get('/{task_id}')
async def retrieve_task(*, db: Session = Depends(dep.get_db),
                        user: m.User = Depends(dep.authorize),
                        task_id: int) -> s.Task:
    task = task_utils.get_task(db, user.id, task_id)
    if not task:
        raise HTTPException(404, 'task not found')
    return s.Task.from_orm(task)

# @router.post('/', status_code=201)
# async def create_task(*, db: Session = Depends(dep.get_db),
#                       user: m.User = Depends(dep.authorize),
#                       body: s.Task) -> s.Task:
#     pass