from fastapi.routing import APIRouter
from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.schema import auth as s
from app.utils import dependency as dep
from app.utils import auth as auth_utils
from app.database.models import User


router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/get-token')
async def get_token(body: s.TokenRequest,
                    db: Session = Depends(dep.get_db)) -> s.TokenResponse:
    token = auth_utils.get_token(db, body.username, body.password)
    if not token:
        raise HTTPException(400, 'Incorrect username or password')
    return s.TokenResponse(token=token)

@router.post('/user', status_code=201)
async def register_user(body: s.RegisterUserRequest,
                        db: Session = Depends(dep.get_db)) -> s.RegisterUserResponse:
    user = auth_utils.register_user(db, body.username, body.password)
    kwargs = body.model_dump()
    kwargs.pop('id')
    kwargs.pop('password')
    auth_utils.update_user(db, user, **kwargs)
    return s.RegisterUserResponse(token=auth_utils.gen_token(user.id))

@router.get('/user')
async def read_user(user: User = Depends(dep.authorize)) -> s.ReadUserResponse:
    return s.ReadUserResponse.model_validate(user)

@router.patch('/user')
async def update_user(body: s.UpdateUserRequest,
                      db: Session = Depends(dep.get_db),
                      user: User = Depends(dep.authorize)) -> s.UpdateUserResponse:
    kwargs = body.model_dump()
    kwargs.pop('id')
    user = auth_utils.update_user(db, user, **kwargs)
    return s.UpdateUserResponse.model_validate(user)

@router.post('/passwd', status_code=204)
async def update_password(body: s.UpdatePasswordRequest,
                          db: Session = Depends(dep.get_db),
                          user: User = Depends(dep.authorize)):
    user = auth_utils.update_password(db, user, 
                                      body.old_password, body.new_password)
    if not user:
        raise HTTPException(400, 'Incorrect password')
