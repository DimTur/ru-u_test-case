import uuid

from pydantic import BaseModel, ConfigDict


class ColorBase(BaseModel):
    hex_color: str


class ColorCreate(ColorBase):
    pass


class ColorUpdate(ColorBase):
    pass


class Color(ColorBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
