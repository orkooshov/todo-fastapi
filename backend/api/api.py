from fastapi.routing import APIRouter
from backend.api.router import auth, task, subtask


router = APIRouter(prefix='/api')
router.include_router(auth.router)
router.include_router(task.router)
router.include_router(subtask.router)
