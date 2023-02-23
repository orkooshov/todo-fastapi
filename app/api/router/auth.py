from fastapi.routing import APIRouter
from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.schema import auth as s
from app.utils import dependency as dep
from app.utils import auth as auth_utils
from app.database.models import User
import bcrypt


router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/get-token')
async def get_token(body: s.TokenRequest,
                    db: Session = Depends(dep.get_db)) -> s.TokenResponse:
    user = auth_utils.authenticate(db, body.username, body.password)
    if not user:
        raise HTTPException(400, 'Incorrect username or password')
    token = auth_utils.gen_token(user.id)
    return s.TokenResponse(token=token)

@router.post('/user', status_code=201)
async def register_user(body: s.RegisterUserRequest,
                        db: Session = Depends(dep.get_db)) -> s.RegisterUserResponse:
    return s.RegisterUserResponse(token=body.username)

@router.get('/user')
async def read_user(user: User = Depends(dep.authorize)) -> s.ReadUserResponse:
    return s.ReadUserResponse.from_orm(user)

@router.patch('/user', status_code=204)
async def update_user(body: s.UpdateUserRequest,
                      db: Session = Depends(dep.get_db),
                      user: User = Depends(dep.authorize)):
    user.username = body.username
    user.first_name = body.firstName
    user.last_name = body.lastName
    user.middle_name = body.middleName
    user.email = body.email
    user.gender = body.gender
    db.commit()

@router.post('/passwd', status_code=204)
async def update_password(body: s.UpdatePasswordRequest,
                          db: Session = Depends(dep.get_db),
                          user: User = Depends(dep.authorize)):
    user = auth_utils.authenticate(db, user.username, body.oldPassword)
    if not user:
        raise HTTPException(400, 'Incorrect password')
    user.password = bcrypt.hashpw(body.newPassword.encode(), bcrypt.gensalt())
    db.commit()
