from typing import Optional

from pydantic import BaseModel, EmailStr, Field, SecretStr, field_serializer


class UserSignup(BaseModel):
    username: str
    password: SecretStr
    email: EmailStr
    date_joined: str

    @field_serializer("password", when_used="always")
    def serialize_password(self, value: SecretStr) -> str:
        return value.get_secret_value()


class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr


class UserSession(BaseModel):
    id: str = Field(alias="_id")
    username: str
    email: EmailStr

    class Config:
        arbitrary_types_allowed = True


class UserProfileRead(BaseModel):
    username: str
    location: Optional[str] = None
    bio: Optional[str] = None
    date_joined: Optional[str] = None


class UserProfileWrite(BaseModel):
    location: str | None = None
    bio: str | None = None
