import uuid

from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict


class ColorBase(BaseModel):
    title: Annotated[str, MinLen(3), MaxLen(32)]
    hex_color: str


class ColorCreate(ColorBase):
    pass


class ColorUpdate(ColorBase):
    pass


class Color(ColorBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
