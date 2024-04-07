import uuid

from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict


class PaletteBase(BaseModel):
    title: Annotated[str, MinLen(3), MaxLen(32)]


class PaletteCreate(PaletteBase):
    pass


class PaletteUpdate(PaletteBase):
    pass


class Palette(PaletteBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
