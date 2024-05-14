from pydantic import BaseModel, Field


class BaseUserNoPassword(BaseModel):
    id: int | None = None
    username: str
    first_name: str = ''
    last_name: str = ''
    middle_name: str = ''
    email: str | None = None
    gender: int = Field(0, ge=0, le=2)

    class Config:
        populate_by_name = True
        from_attributes = True


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
    username: str | None = None


class UpdateUserResponse(BaseUserNoPassword):
    pass


class UpdatePasswordRequest(BaseModel):
    old_password: str = Field(alias='oldPassword')
    new_password: str = Field(alias='newPassword')
