from pydantic import BaseModel


class TokenResponse(BaseModel):
    token_type: str = "Bearer"
    access_token: str
    refresh_token: str


class UserLogin(BaseModel):
    username: str
    password: str