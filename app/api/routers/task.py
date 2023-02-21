from fastapi.routing import APIRouter
from app.database.models import Task
from app.database.connection import create_session


router = APIRouter(prefix='/task', tags=['task'])

@router.get('/')
async def get_tasks():
    with create_session() as dbs:
        tasks = dbs.query(Task).all()
    return tasks
