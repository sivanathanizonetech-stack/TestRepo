from app.schemas.base import SchemaModel


class LoginRequest(SchemaModel):
    username: str
    password: str


class TokenResponse(SchemaModel):
    access_token: str
    token_type: str = "bearer"
    role: str

