from app.schemas.base import CamelModel
from app.schemas.common import UserRead


class LoginRequest(CamelModel):
    username: str
    password: str


class TokenResponse(CamelModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead
