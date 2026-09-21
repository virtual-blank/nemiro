from pydantic import BaseModel, ConfigDict, SecretStr
import uuid
from datetime import datetime

class UserCreateSchema(BaseModel):
    model_config=ConfigDict(
        str_strip_whitespace=True
    )
    username: str
    password_str: SecretStr
    

class UserOutputSchema(BaseModel):
    model_config=ConfigDict(
        from_attributes=True
    )
    id: uuid.UUID
    username: str
    is_admin: bool


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class AuthOutputSchema(BaseModel):
    user: UserOutputSchema
    token: TokenSchema
