from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginResponse(BaseModel):
    id: str
    email: str
    full_name: str | None
    role_id: int
    role_name: str
    access_token: str
    token_type: str = "bearer"

class UserInfoResponse(BaseModel):
    id: str
    email: str
    full_name: str | None
    role_id: int
    role_name: str

class UserInfoResponseWithPermissions(BaseModel):
    id: str
    email: str
    full_name: str | None
    role_id: int
    role_name: str
    permissions: list[str]
