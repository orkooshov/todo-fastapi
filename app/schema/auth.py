from pydantic import BaseModel


class BaseUserNoPassword(BaseModel):
    id: int | None = None
    username: str
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    email: str | None = None
    gender: str | None = None


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
    old_password: str
    new_password: str


class UpdatePasswordResponse(TokenResponse):
    pass
