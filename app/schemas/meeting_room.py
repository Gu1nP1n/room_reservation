from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MeetingRoomBase(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description='Название переговорной комнаты'
    )
    description: Optional[str] = Field(
        None,
        description='Описание переговорной комнаты'
    )


class MeetingRoomCreate(MeetingRoomBase):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description='Название переговорной комнаты '
    )


class MeetingRoomDB(MeetingRoomCreate):
    id: int = Field(
        description='ID переговорной комнаты'
    )
    model_config = ConfigDict(from_attributes=True)


class MeetingRoomUpdate(MeetingRoomBase):

    @field_validator('name')
    @classmethod
    def name_cannot_be_null(cls, value):
        if value is None:
            error = 'Имя переговорки не может быть пустым!'
            raise ValueError(error)
        return value
