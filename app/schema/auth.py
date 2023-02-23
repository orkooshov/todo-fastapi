from pydantic import BaseModel, Field


class BaseUserNoPassword(BaseModel):
    id: int | None = None
    username: str
    firstName: str = ''
    lastName: str = ''
    middleName: str = ''
    email: str | None = None
    gender: int = Field(0, ge=0, le=2)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class BaseUser(BaseUserNoPassword):
    password: str


class TokenRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    token: str


class RegisterUserRequest(BaseUser):
    pass


class RegisterUserResponse(TokenResponse):
    pass


class ReadUserResponse(BaseUserNoPassword):
    pass


class UpdateUserRequest(BaseUserNoPassword):
    pass


class UpdatePasswordRequest(BaseModel):
    oldPassword: str
    newPassword: str
