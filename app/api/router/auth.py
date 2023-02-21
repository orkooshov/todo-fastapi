from fastapi.routing import APIRouter
from app.schema import auth as s


router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/get-token')
async def get_token(body: s.TokenRequest) -> s.TokenResponse:
    return s.TokenResponse(token=f'{body.username} {body.password}')

@router.post('/user', status_code=201)
async def register_user(body: s.RegisterUserRequest) -> s.RegisterUserResponse:
    return s.RegisterUserResponse(token=body.username)

@router.get('/user/{user_id}')
async def read_user(user_id: int) -> s.ReadUserResponse:
    return s.ReadUserResponse(id=user_id, username='test')

@router.put('/user/{user_id}', status_code=204)
async def update_user(user_id: int, body: s.UpdateUserRequest):
    return

@router.post('/passwd')
async def update_password(body: s.UpdatePasswordRequest) -> s.UpdatePasswordResponse:
    return s.UpdatePasswordResponse(token=body.new_password)
