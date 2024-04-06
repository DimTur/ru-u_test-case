import uuid

from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    name: Annotated[str, MinLen(3), MaxLen(32)]
    login: Annotated[str, MinLen(3), MaxLen(32)]


class UserCreate(UserBase):
    hashed_password: str


class UserUpdatePartial(UserCreate):
    pass


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
