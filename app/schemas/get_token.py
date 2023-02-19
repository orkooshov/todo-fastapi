from pydantic import BaseModel


class GetTokenRequest(BaseModel):
    username: str
    password: str


class GetTokenResponse(BaseModel):
    token: str
